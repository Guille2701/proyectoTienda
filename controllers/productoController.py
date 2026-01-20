import os
from flask import render_template, request, redirect, url_for, current_app, session
from werkzeug.utils import secure_filename
from models import db, Producto

class ProductoController:
    
    # --- LISTAR ---
    @staticmethod
    def index():
        if session.get('role') == 'admin':
            lista_productos = Producto.query.all()
        else:
            lista_productos = Producto.query.filter(Producto.visible == True, Producto.stock > 0).all()
        
        return render_template('main.html', products=lista_productos)

    # --- CREAR ---
    @staticmethod
    def create():
        if request.method == 'POST':
            nombre = request.form['nombre']
            precio = float(request.form['precio'])
            stock = int(request.form['stock'])
            
            archivo = request.files.get('imagen')
            nombre_imagen = None
            
            if archivo and archivo.filename != '':
                nombre_imagen = secure_filename(archivo.filename)
                ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_imagen)
                archivo.save(ruta_guardado)
            
            nuevo_producto = Producto(
                nombre=nombre, 
                precio=precio, 
                stock=stock, 
                imagen_url=nombre_imagen
            )
            
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
            
            archivo = request.files.get('imagen')
            
            if archivo and archivo.filename != '':
                nombre_imagen = secure_filename(archivo.filename)
                ruta_guardado = os.path.join(current_app.config['UPLOAD_FOLDER'], nombre_imagen)
                archivo.save(ruta_guardado)
                
                producto.imagen_url = nombre_imagen

            db.session.commit()
            return redirect(url_for('index'))

        return render_template('edit_product.html', product=producto)

    # --- BORRAR ---
    @staticmethod
    def delete(id_producto):
        producto = Producto.query.get_or_404(id_producto)
        
        producto.visible = not producto.visible
        db.session.commit()
        
        return redirect(url_for('index'))