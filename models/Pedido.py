from .db import db
from datetime import datetime

class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    total = db.Column(db.Float, nullable=False)
    
    # Relationships
    detalles = db.relationship('Detalle_Pedido', backref='pedido', lazy=True)

    def __repr__(self):
        return f'<Pedido {self.id}>'
