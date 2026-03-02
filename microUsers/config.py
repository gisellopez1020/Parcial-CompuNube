class Config:
    MYSQL_HOST = 'mysql'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'myflaskapp'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'
    
    # Consul Configuration
    CONSUL_HOST = 'consul'
    CONSUL_PORT = 8500
    SERVICE_NAME = 'users-service'
    SERVICE_PORT = 5002
    SERVICE_HOST = 'microUsers'

