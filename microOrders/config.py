class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@mysql/orders_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_NAME = 'orders-service'
    SERVICE_HOST = '0.0.0.0'
    SERVICE_PORT = 5004
    SECRET_KEY = 'orders-secret-key'