import os
from flask import Flask, render_template, redirect, url_for
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
# ELIMINAR PRODUCTO
# =========================
@app.route(
    "/productos/eliminar/<int:id>",
    methods=["POST"]
)
def eliminar_producto(id):

    producto = Producto.query.get_or_404(id)

    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)