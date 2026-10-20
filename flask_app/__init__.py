from flask import Flask, render_template
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

from flask_app.controllers.usuarios_controllers import usuarios_bp
from flask_app.controllers.entradas_controllers import entradas_bp

app.register_blueprint(usuarios_bp)
app.register_blueprint(entradas_bp)


@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html'), 404
