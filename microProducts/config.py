class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@mysql/products_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVICE_NAME = 'products-service'
    SERVICE_HOST = '0.0.0.0'
    SERVICE_PORT = 5003