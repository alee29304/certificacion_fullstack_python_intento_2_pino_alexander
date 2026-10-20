from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[\w.+-]+@[\w-]+\.[\w.-]+$')

class Usuario:
    def __init__(self, data):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.edad = data['edad']
        self.password = data['password']
        self.created_at = data['created_at']

    @staticmethod
    def validar_registro(data):
        es_valido = True

        if not data['nombre'].strip():
            flash('El nombre es obligatorio.', 'registro')
            es_valido = False

        if not data['apellido'].strip():
            flash('El apellido es obligatorio.', 'registro')
            es_valido = False

        if not EMAIL_REGEX.match(data['correo']):
            flash('Ingresa un correo válido.', 'registro')
            es_valido = False

        if not data['edad'].isdigit() or not 1 <= int(data['edad']) <= 120:
            flash('Ingresa una edad válida.', 'registro')
            es_valido = False

        if len(data['password']) < 8:
            flash('La contraseña debe tener al menos 8 caracteres.', 'registro')
            es_valido = False

        if data['password'] != data['confirmar_password']:
            flash('Las contraseñas no coinciden.', 'registro')
            es_valido = False

        return es_valido

    @classmethod
    def correo_existe(cls, correo):
        query = "SELECT * FROM usuarios WHERE correo = %(correo)s;"
        resultado = connectToMySQL('esquema_entradas').query_db(
            query, {'correo': correo}
        )
        return len(resultado) > 0

    @classmethod
    def crear(cls, data):
        password_hash = bcrypt.generate_password_hash(
            data['password']
        ).decode('utf-8')

        query = """
            INSERT INTO usuarios
            (nombre, apellido, correo, edad, password)
            VALUES (%(nombre)s, %(apellido)s, %(correo)s, %(edad)s, %(password)s);
        """

        datos = {
            'nombre': data['nombre'].strip(),
            'apellido': data['apellido'].strip(),
            'correo': data['correo'].strip().lower(),
            'edad': int(data['edad']),
            'password': password_hash
        }

        return connectToMySQL('esquema_entradas').query_db(query, datos)

    @classmethod
    def buscar_por_correo(cls, correo):
        query = "SELECT * FROM usuarios WHERE correo = %(correo)s;"
        resultado = connectToMySQL('esquema_entradas').query_db(
            query, {'correo': correo.strip().lower()}
        )

        if resultado:
            return cls(resultado[0])

        return None

    @staticmethod
    def verificar_password(password, password_hash):
        return bcrypt.check_password_hash(password_hash, password)