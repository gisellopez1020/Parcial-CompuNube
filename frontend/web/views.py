from flask import Flask, render_template, jsonify
from flask_cors import CORS
import consul

app = Flask(__name__)
app.secret_key = 'secret123'
CORS(app, supports_credentials=True)
app.config.from_object('config.Config')

# Configurar Consul
consul_client = consul.Consul(host='consul', port=8500)

# Aplicar configuración remota desde Consul KV
try:
    _, data = consul_client.kv.get('frontend-service/', recurse=True)
    if data:
        for item in data:
            key = item['Key'].replace('frontend-service/', '')
            app.config[key] = item['Value'].decode('utf-8') if item['Value'] else None
except Exception as e:
    print(f"[WARN] No se pudo cargar config remota de Consul: {e}")

# Registrar servicio en Consul
try:
    consul_client.agent.service.register(
        name=app.config['SERVICE_NAME'],
        port=int(app.config['SERVICE_PORT']),
        check=consul.Check.http(
            f"http://{app.config['SERVICE_HOST']}:{app.config['SERVICE_PORT']}/health",
            interval='10s'
        )
    )
except Exception as e:
    print(f"[WARN] No se pudo registrar el servicio en Consul: {e}")

# Ruta para renderizar el template index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Ruta para renderizar el template users.html
@app.route('/users')
def users():
    return render_template('users.html')

# Ruta para renderizar el template products.html
@app.route('/products')
def products():
    return render_template('products.html')

# Ruta para renderizar el template orders.html
@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/editUser/<string:id>')
def edit_user(id):
    print("id recibido", id)
    return render_template('editUser.html', id=id)

@app.route('/editProduct/<string:id>')
def edit_product(id):
    print("id recibido", id)
    return render_template('editProduct.html', id=id)

@app.route('/editOrder/<string:id>')
def edit_order(id):
    print("id recibido",id)
    return render_template('editOrder.html', id=id)

# Healthcheck endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'frontend-service'}), 200

if __name__ == '__main__':
    app.run()