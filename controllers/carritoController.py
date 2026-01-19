from flask import session, redirect, url_for, render_template
from datetime import datetime
from collections import Counter
from models import db, Producto, Pedido, Detalle_Pedido

class CarritoController:
    
    # --- AÑADIR (Botón +) ---
    @staticmethod
    def add(id_producto):
        if 'carrito' not in session:
            session['carrito'] = []
        
        carrito = session['carrito']
        carrito.append(id_producto)
        session['carrito'] = carrito
        return redirect(url_for('view_cart'))

    # --- QUITAR UNO (Botón -) --- NUEVO MÉTODO
    @staticmethod
    def remove_one(id_producto):
        if 'carrito' in session:
            carrito = session['carrito']
            # Si el producto está en el carrito, quitamos solo la primera coincidencia
            if id_producto in carrito:
                carrito.remove(id_producto)
                session['carrito'] = carrito
        return redirect(url_for('view_cart'))

    # --- MOSTRAR CESTA ---
    @staticmethod
    def show():
        ids_carrito = session.get('carrito', [])
        
        conteo_productos = Counter(ids_carrito)
        ids_unicos = list(conteo_productos.keys())
        
        productos_para_mostrar = []
        subtotal = 0
        
        if ids_unicos:
            productos_bd = Producto.query.filter(Producto.id.in_(ids_unicos)).all()
            
            for prod in productos_bd:
                cantidad = conteo_productos[prod.id]
                prod.quantity = cantidad 
                
                subtotal += prod.precio * cantidad
                productos_para_mostrar.append(prod)
            
        # Cálculos económicos
        impuestos = subtotal * 0.21
        total_final = subtotal + impuestos
            
        return render_template('cart.html', 
                               products=productos_para_mostrar, 
                               subtotal=subtotal,
                               tax=impuestos,
                               total=total_final)

    # --- PROCESAR COMPRA ---
    @staticmethod
    def checkout():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        
        ids_carrito = session.get('carrito', [])
        if not ids_carrito:
            return redirect(url_for('index'))

        conteo_productos = Counter(ids_carrito)
        ids_unicos = list(conteo_productos.keys())

        nuevo_pedido = Pedido(
            usuario_id=session['user_id'],
            fecha=datetime.now(),
            total=0 
        )
        db.session.add(nuevo_pedido)
        db.session.flush()
        
        total_calculado = 0
        productos_bd = Producto.query.filter(Producto.id.in_(ids_unicos)).all()

        for prod in productos_bd:
            cantidad = conteo_productos[prod.id]
            
            detalle = Detalle_Pedido(
                pedido_id=nuevo_pedido.id,
                producto_id=prod.id,
                cantidad=cantidad,
                precio_unitario=prod.precio
            )
            
            if prod.stock >= cantidad:
                prod.stock -= cantidad
            
            total_calculado += (prod.precio * cantidad)
            db.session.add(detalle)
        
        nuevo_pedido.total = total_calculado * 1.21
        
        db.session.commit()
        session.pop('carrito', None)
        
        return render_template('cart.html', success=True)