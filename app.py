from flask import Flask
from models import db
from controllers.usuarioController import UsuarioController
from controllers.productoController import ProductoController
from controllers.carritoController import CarritoController

app = Flask(__name__)

# --- CONFIGURACIÓN ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/python_proyecto_tienda'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mi_clave_secreta_super_segura'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)


# --- PÁGINA PRINCIPAL (Catálogo) ---
@app.route('/')
def index():
    return ProductoController.index()

# --- RUTAS DE USUARIO (Login/Registro) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    return UsuarioController.login()

@app.route('/register', methods=['GET', 'POST'])
def register():
    return UsuarioController.register()

@app.route('/logout')
def logout():
    return UsuarioController.logout()

# --- RUTAS DE PRODUCTO (CRUD) ---
@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    return ProductoController.create()

@app.route('/product/edit/<int:id_producto>', methods=['GET', 'POST'])
def edit_product(id_producto):
    return ProductoController.update(id_producto)

@app.route('/product/delete/<int:id_producto>')
def delete_product(id_producto):
    return ProductoController.delete(id_producto)

# --- RUTAS DE CARRITO Y COMPRA ---
@app.route('/cart')
def view_cart():
    return CarritoController.show()

@app.route('/cart/add/<int:id_producto>')
def add_to_cart(id_producto):
    return CarritoController.add(id_producto)

@app.route('/cart/remove/<int:id_producto>')
def remove_from_cart(id_producto):
    return CarritoController.remove_one(id_producto)

@app.route('/checkout')
def checkout():
    return CarritoController.checkout()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)