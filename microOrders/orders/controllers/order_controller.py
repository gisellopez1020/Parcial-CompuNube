from flask import Blueprint, jsonify, request, session
import requests
import consul

order_controller = Blueprint('order_controller', __name__)

def get_products_url():
    """Descubre dinámicamente la URL de microProducts usando Consul."""
    try:
        consul_client = consul.Consul(host='consul', port=8500)
        _, services = consul_client.health.service('products-service', passing=True)
        if not services:
            return None
        service = services[0]['Service']
        host = service['Address'] or 'microproducts'
        port = service['Port']
        return f"http://{host}:{port}"
    except Exception as e:
        print(f"[WARN] No se pudo descubrir products-service en Consul: {e}")
        return None

@order_controller.route('/api/orders', methods=['GET'])
def get_all_orders():
    from orders.models.order_model import Order
    try:
        orders = Order.query.all()
        return jsonify([o.to_dict() for o in orders]), 200
    except Exception as e:
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    from orders.models.order_model import Order
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'message': 'Orden no encontrada'}), 404
        return jsonify(order.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    from orders.models.order_model import Order, OrderItem
    from db.db import db

    data = request.get_json()

    user_name  = data.get('username')
    user_email = data.get('email')

    if not user_name or not user_email:
        return jsonify({'message': 'Información de usuario inválida'}), 400

    products = data.get('products')
    if not products or not isinstance(products, list):
        return jsonify({'message': 'Falta o es inválida la información de los productos'}), 400

    # Descubrir URL de microProducts via Consul
    products_url = get_products_url()
    if not products_url:
        return jsonify({'message': 'No se pudo conectar con el servicio de productos'}), 500

    total = 0
    order_items = []

    for item in products:
        product_id = item.get('product_id')
        quantity   = item.get('quantity')

        if not product_id or not quantity:
            return jsonify({'message': 'Cada producto debe tener product_id y quantity'}), 400

        # Consultar el producto
        try:
            resp = requests.get(f"{products_url}/api/products/{product_id}")
        except Exception as e:
            return jsonify({'message': f'Error al contactar microProducts: {str(e)}'}), 500

        if resp.status_code == 404:
            return jsonify({'message': f'Producto {product_id} no existe'}), 404
        if resp.status_code != 200:
            return jsonify({'message': 'Error al obtener información del producto'}), 500

        product = resp.json()
        available_quantity = product.get('quantity', 0)
        price = product.get('price', 0)
        name = product.get('name', 'Producto Desconocido')

        if available_quantity < quantity:
            return jsonify({'message': f'Inventario insuficiente para el producto {product_id}'}), 409

        total += price * quantity
        order_items.append({
            'product_id': product_id,
            'product_name': name,
            'quantity': quantity,
            'price': price,
            'new_quantity': available_quantity - quantity
        })

    # Actualizar inventario en microProducts
    for item in order_items:
        try:
            resp = requests.put(
                f"{products_url}/api/products/{item['product_id']}",
                json={'quantity': item['new_quantity']}
            )
            if resp.status_code != 200:
                return jsonify({'message': f"Error actualizando inventario del producto {item['product_id']}"}), 500
        except Exception as e:
            return jsonify({'message': f'Error al actualizar inventario: {str(e)}'}), 500

    # Guardar la orden en la base de datos
    try:
        new_order = Order(user_name=user_name, user_email=user_email, total=total)
        db.session.add(new_order)
        db.session.flush()

        for item in order_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product_id'],
                product_name=item['product_name'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)

        db.session.commit()
        return jsonify({'message': 'Orden creada exitosamente', 'order_id': new_order.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@order_controller.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    from orders.models.order_model import Order
    from db.db import db
    try:
        order = Order.query.get(order_id)
        if not order:
            return jsonify({'message': 'Orden no encontrada'}), 404
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Orden eliminada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno: {str(e)}'}), 500