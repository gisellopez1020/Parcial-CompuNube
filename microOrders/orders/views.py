from flask import Flask, jsonify
from orders.controllers.order_controller import order_controller
from db.db import db
from flask_cors import CORS
import consul

app = Flask(__name__)
app.config.from_object('config.Config')
db.init_app(app)

# Crear tablas automáticamente
with app.app_context():
    db.create_all()

# Configurar Consul
consul_client = consul.Consul(host='consul', port=8500)

# Registrar servicio en Consul
try:
    consul_client.agent.service.register(
        name=app.config['SERVICE_NAME'],
        port=int(app.config['SERVICE_PORT']),
        check=consul.Check.http(
            f"http://microorders:{app.config['SERVICE_PORT']}/health",
            interval='10s'
        )
    )
except Exception as e:
    print(f"[WARN] No se pudo registrar en Consul: {e}")

app.register_blueprint(order_controller)
CORS(app, resources={r"/api/*": {"origins": "http://192.168.80.3:5001"}}, supports_credentials=True)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'orders-service'}), 200

if __name__ == '__main__':
    app.run()