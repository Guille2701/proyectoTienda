from .db import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    visible = db.Column(db.Boolean, default=True, nullable=False)
    
    # Relationships
    detalles = db.relationship('Detalle_Pedido', backref='producto', lazy=True)

    def __repr__(self):
        return f'<Producto {self.nombre}>'
