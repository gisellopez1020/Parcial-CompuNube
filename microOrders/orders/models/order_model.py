from db.db import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = 'orders'

    id          = db.Column(db.Integer, primary_key=True)
    user_name   = db.Column(db.String(100), nullable=False)
    user_email  = db.Column(db.String(100), nullable=False)
    total       = db.Column(db.Float, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)
    items       = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'user_email': self.user_email,
            'total': self.total,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items]
        }

class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    price      = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'quantity': self.quantity,
            'price': self.price,
            'subtotal': self.quantity * self.price
        }