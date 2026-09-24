
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================
# MODELO CATEGORIA
# =========================
class Categoria(db.Model):
    __tablename__ = "categorias"

    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))


# =========================
# MODELO MARCA
# =========================
class Marca(db.Model):
    __tablename__ = "marcas"

    id_marca = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    pais_origen = db.Column(db.String(100))


# =========================
# MODELO PRODUCTO
# =========================
class Producto(db.Model):
    __tablename__ = "productos"

    id_producto = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.String(255))
    precio = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    id_categoria = db.Column(
        db.Integer,
        db.ForeignKey("categorias.id_categoria"),
        nullable=False
    )

    id_marca = db.Column(
        db.Integer,
        db.ForeignKey("marcas.id_marca"),
        nullable=False
    )

    fecha_registro = db.Column(db.DateTime)

    categoria = db.relationship("Categoria")
    marca = db.relationship("Marca")


# =========================
# LISTAR PRODUCTOS
# =========================
@app.route("/")
def index():

    productos = Producto.query.order_by(
        Producto.id_producto
    ).all()

    return render_template(
        "index.html",
        productos=productos
    )


# =========================
# ACTUALIZAR PRODUCTO
# =========================
@app.route(
    "/productos/actualizar/<int:id>",
    methods=["GET", "POST"]
)
def actualizar_producto(id):

    producto = Producto.query.get_or_404(id)
# AGREGAR PRODUCTO
# =========================
@app.route("/productos/crear", methods=["GET", "POST"])
def crear_producto():

    categorias = Categoria.query.order_by(
        Categoria.nombre
    ).all()

    marcas = Marca.query.order_by(
        Marca.nombre
    ).all()

    if request.method == "POST":

        producto.nombre = request.form["nombre"]
        producto.descripcion = request.form["descripcion"]
        producto.precio = request.form["precio"]
        producto.stock = request.form["stock"]
        producto.id_categoria = request.form["id_categoria"]
        producto.id_marca = request.form["id_marca"]

        nuevo_producto = Producto(
            nombre=request.form["nombre"],
            descripcion=request.form["descripcion"],
            precio=request.form["precio"],
            stock=request.form["stock"],
            id_categoria=request.form["id_categoria"],
            id_marca=request.form["id_marca"]
        )

        db.session.add(nuevo_producto)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template(
        "update_products.html",
        producto=producto,
        "create_products.html",
        categorias=categorias,
        marcas=marcas
    )


if __name__ == "__main__":
    app.run(debug=True)

    