from flask import render_template, request, redirect, url_for
from models import db, Producto

class ProductoController:
    
    # --- LISTAR ---
    @staticmethod
    def index():
        lista_productos = Producto.query.all()
        return render_template('main.html', products=lista_productos)

    # --- CREAR ---
    @staticmethod
    def create():
        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            nuevo_producto = Producto(nombre=nombre, precio=precio, stock=stock)
            
            db.session.add(nuevo_producto)
            db.session.commit()
            
            return redirect(url_for('index'))
            
        return render_template('add_product.html')

    # --- EDITAR ---
    @staticmethod
    def update(id_producto):
        producto = Producto.query.get_or_404(id_producto)

        if request.method == 'POST':
            producto.nombre = request.form['nombre']
            producto.precio = float(request.form['precio'])
            producto.stock = int(request.form['stock'])

            db.session.commit()
            return redirect(url_for('index'))

        return render_template('edit_product.html', product=producto)

    # --- BORRAR ---
    @staticmethod
    def delete(id_producto):
        producto = Producto.query.get_or_404(id_producto)
        
        db.session.delete(producto)
        db.session.commit()
        
        return redirect(url_for('index'))