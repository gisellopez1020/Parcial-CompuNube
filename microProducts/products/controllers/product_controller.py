from flask import Blueprint, jsonify, request
from products.models.product_model import Product
from db.db import db

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products', methods=['GET'])
def get_products():
    try:
        products = Product.query.all()
        return jsonify([p.to_dict() for p in products]), 200
    except Exception as e:
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Producto no encontrado'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@product_controller.route('/api/products', methods=['POST'])
def create_product():
    try:
        data = request.get_json()
        name     = data.get('name')
        price    = data.get('price')
        quantity = data.get('quantity')

        if not name or price is None or quantity is None:
            return jsonify({'message': 'Faltan campos obligatorios: name, price, quantity'}), 400

        new_product = Product(
            name=name,
            price=float(price),
            quantity=int(quantity)
        )
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Producto creado exitosamente', 'product': new_product.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Producto no encontrado'}), 404

        data = request.get_json()
        if 'name'     in data: product.name     = data['name']
        if 'price'    in data: product.price    = float(data['price'])
        if 'quantity' in data: product.quantity = int(data['quantity'])

        db.session.commit()
        return jsonify({'message': 'Producto actualizado', 'product': product.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno: {str(e)}'}), 500

@product_controller.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Producto no encontrado'}), 404

        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Producto eliminado exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error interno: {str(e)}'}), 500