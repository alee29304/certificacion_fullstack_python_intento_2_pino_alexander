from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import date

class Entrada:

    def __init__(self, data):
        self.id = data['id']
        self.fecha = data['fecha']
        self.notas = data['notas']
        self.usuario_id = data['usuario_id']
        self.created_at = data['created_at']

    @staticmethod
    def validar(data):
        es_valido = True
        fecha = data.get('fecha', '').strip()
        notas = data.get('notas', '').strip()

        if not fecha:
            flash('La fecha es obligatoria.', 'entrada')
            es_valido = False
        else:
            try:
                fecha_convertida = date.fromisoformat(fecha)
                if fecha_convertida > date.today():
                    flash('La fecha no puede estar en el futuro.', 'entrada')
                    es_valido = False
            except ValueError:
                flash('Ingresa una fecha válida.', 'entrada')
                es_valido = False

        if not notas:
            flash('Las notas son obligatorias.', 'entrada')
            es_valido = False

        return es_valido

    @classmethod
    def crear(cls, data):
        query = """
            INSERT INTO entradas (fecha, notas, usuario_id)
            VALUES (%(fecha)s, %(notas)s, %(usuario_id)s);
        """
        return connectToMySQL('esquema_entradas').query_db(query, data)

    @classmethod
    def obtener_por_usuario(cls, usuario_id):
        query = """
            SELECT * FROM entradas
            WHERE usuario_id = %(usuario_id)s
            ORDER BY fecha DESC, id DESC;
        """
        resultados = connectToMySQL('esquema_entradas').query_db(
            query, {'usuario_id': usuario_id}
        )
        return [cls(entrada) for entrada in resultados]

    @classmethod
    def obtener_por_id_y_usuario(cls, data):
        query = """
            SELECT * FROM entradas
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        resultados = connectToMySQL('esquema_entradas').query_db(query, data)

        if resultados:
            return cls(resultados[0])

        return None

    @classmethod
    def actualizar(cls, data):
        query = """
            UPDATE entradas
            SET fecha = %(fecha)s, notas = %(notas)s
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL('esquema_entradas').query_db(query, data)

    @classmethod
    def borrar(cls, data):
        query = """
            DELETE FROM entradas
            WHERE id = %(id)s AND usuario_id = %(usuario_id)s;
        """
        return connectToMySQL('esquema_entradas').query_db(query, data)

    @classmethod
    def buscar(cls, termino, usuario_id):
        query = """
            SELECT * FROM entradas
            WHERE notas LIKE %(termino)s
            AND usuario_id = %(usuario_id)s
            ORDER BY fecha DESC, id DESC;
        """
        resultados = connectToMySQL('esquema_entradas').query_db(
            query,
            {
                'termino': f'%{termino}%',
                'usuario_id': usuario_id
            }
        )
        return [cls(entrada) for entrada in resultados]
