from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.entrada import Entrada
from datetime import date

entradas_bp = Blueprint('entradas', __name__)


def usuario_requerido():
    if 'usuario_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página.', 'login')
        return False
    return True


@entradas_bp.route('/entradas')
def entradas_inicio():
    if not usuario_requerido():
        return redirect('/login/vista')

    entradas = Entrada.obtener_por_usuario(session['usuario_id'])
    return render_template('inicio.html', entradas=entradas)


@entradas_bp.route('/entradas/nueva')
def nueva_entrada():
    if not usuario_requerido():
        return redirect('/login/vista')

    return render_template(
        'nueva_entrada.html',
        fecha_hoy=date.today().isoformat()
    )


@entradas_bp.route('/entradas/crear', methods=['POST'])
def crear_entrada():
    if not usuario_requerido():
        return redirect('/login/vista')

    data = {
        'fecha': request.form.get('fecha', '').strip(),
        'notas': request.form.get('notas', '').strip(),
        'usuario_id': session['usuario_id']
    }

    if not Entrada.validar(data):
        return redirect('/entradas/nueva')

    Entrada.crear(data)
    flash('Entrada creada correctamente.', 'entrada')
    return redirect('/entradas')


@entradas_bp.route('/entradas/editar/<int:id>')
def editar_entrada(id):
    if not usuario_requerido():
        return redirect('/login/vista')

    entrada = Entrada.obtener_por_id_y_usuario({
        'id': id,
        'usuario_id': session['usuario_id']
    })

    if not entrada:
        flash('La entrada no existe o no tienes permiso para verla.', 'entrada')
        return redirect('/entradas')

    return render_template(
        'editar_entrada.html',
        entrada=entrada,
        fecha_hoy=date.today().isoformat()
    )


@entradas_bp.route('/entradas/actualizar/<int:id>', methods=['POST'])
def actualizar_entrada(id):
    if not usuario_requerido():
        return redirect('/login/vista')

    data = {
        'id': id,
        'fecha': request.form.get('fecha', '').strip(),
        'notas': request.form.get('notas', '').strip(),
        'usuario_id': session['usuario_id']
    }

    entrada = Entrada.obtener_por_id_y_usuario({
        'id': id,
        'usuario_id': session['usuario_id']
    })

    if not entrada:
        flash('La entrada no existe o no tienes permiso para editarla.', 'entrada')
        return redirect('/entradas')

    if not Entrada.validar(data):
        return redirect(f'/entradas/editar/{id}')

    Entrada.actualizar(data)
    flash('Entrada actualizada correctamente.', 'entrada')
    return redirect('/entradas')


@entradas_bp.route('/entradas/borrar/<int:id>', methods=['POST'])
def borrar_entrada(id):
    if not usuario_requerido():
        return redirect('/login/vista')

    eliminada = Entrada.borrar({
        'id': id,
        'usuario_id': session['usuario_id']
    })

    if eliminada:
        flash('Entrada eliminada correctamente.', 'entrada')
    else:
        flash(
            'No se encontró la entrada o no tienes permiso para borrarla.',
            'entrada'
        )

    return redirect('/entradas')


@entradas_bp.route('/entradas/ver/<int:id>')
def ver_entrada(id):
    if not usuario_requerido():
        return redirect('/login/vista')

    entrada = Entrada.obtener_por_id_y_usuario({
        'id': id,
        'usuario_id': session['usuario_id']
    })

    if not entrada:
        flash('La entrada no existe o no tienes permiso para verla.', 'entrada')
        return redirect('/entradas')

    return render_template('ver_entrada.html', entrada=entrada)


@entradas_bp.route('/buscar')
def buscar_entradas():
    if not usuario_requerido():
        return redirect('/login/vista')

    termino = request.args.get('termino', '').strip()
    entradas = (
        Entrada.buscar(termino, session['usuario_id'])
        if termino else []
    )

    return render_template(
        'buscar.html',
        entradas=entradas,
        termino=termino
    )
