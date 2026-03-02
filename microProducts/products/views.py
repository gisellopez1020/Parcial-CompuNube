from flask import Flask, jsonify
from products.controllers.product_controller import product_controller
from db.db import db
from flask_cors import CORS
import consul

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Configurar Consul
consul_client = consul.Consul(host='consul', port=8500)

# Aplicar configuración remota desde Consul KV
try:
    _, data = consul_client.kv.get('products-service/', recurse=True)
    if data:
        for item in data:
            key = item['Key'].replace('products-service/', '')
            app.config[key] = item['Value'].decode('utf-8') if item['Value'] else None
except Exception as e:
    print(f"[WARN] No se pudo cargar config remota de Consul: {e}")

# Registrar servicio en Consul
try:
    consul_client.agent.service.register(
        name=app.config['SERVICE_NAME'],
        port=int(app.config['SERVICE_PORT']),
        check=consul.Check.http(
            f"http://microproducts:{app.config['SERVICE_PORT']}/health",
            interval='10s'
        )
    )
except Exception as e:
    print(f"[WARN] No se pudo registrar el servicio en Consul: {e}")

# Registrando el blueprint del controlador de productos
app.register_blueprint(product_controller)
CORS(app, resources={r"/api/*": {"origins": "http://192.168.80.3:5001"}}, supports_credentials=True)

# Healthcheck endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'products-service'}), 200

if __name__ == '__main__':
    app.run()