from .db import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    # Relationships
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)

    def __repr__(self):
        return f'<Usuario {self.username}>'
