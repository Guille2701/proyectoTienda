from flask import session, redirect, url_for, render_template
from datetime import datetime
from models import db, Producto, Pedido, Detalle_Pedido

class CarritoController:
    
    # Añadir a la cesta (Sesión temporal)
    @staticmethod
    def add(id_producto):
        if 'carrito' not in session:
            session['carrito'] = []
        
        carrito = session['carrito']
        carrito.append(id_producto)
        session['carrito'] = carrito
        return redirect(url_for('index'))

    # Mostrar la cesta
    @staticmethod
    def show():
        ids_carrito = session.get('carrito', [])
        productos_en_carrito = []
        total = 0
        
        if ids_carrito:
            productos_en_carrito = Producto.query.filter(Producto.id.in_(ids_carrito)).all()
            total = sum(p.precio for p in productos_en_carrito)
            
        return render_template('cart.html', products=productos_en_carrito, total=total)

    # PROCESAR COMPRA (Checkout)
    @staticmethod
    def checkout():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        ids_carrito = session.get('carrito', [])
        if not ids_carrito:
            return redirect(url_for('index'))

        nuevo_pedido = Pedido(
            usuario_id=session['user_id'],
            fecha=datetime.now(),
            total=0
        )
        
        db.session.add(nuevo_pedido)
        db.session.flush()
        
        total_calculado = 0
        productos_bd = Producto.query.filter(Producto.id.in_(ids_carrito)).all()

        for prod in productos_bd:
            detalle = Detalle_Pedido(
                pedido_id=nuevo_pedido.id,
                producto_id=prod.id,
                cantidad=1, 
                precio_unitario=prod.precio
            )
            
            if prod.stock > 0:
                prod.stock -= 1
            
            total_calculado += prod.precio
            db.session.add(detalle)
        
        nuevo_pedido.total = total_calculado
        db.session.commit()
        
        session.pop('carrito', None)
        
        return render_template('cart.html', success=True)