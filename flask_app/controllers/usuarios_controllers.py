from flask import Blueprint, render_template, request, redirect, session, flash
from flask_app.models.usuario import Usuario
usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/')
def pagina_inicio():
    if 'usuario_id' in session:
        return redirect('/entradas')
    return redirect('/login/vista')

@usuarios_bp.route('/login/vista')
def login_vista():
    if 'usuario_id' in session:
        return redirect('/entradas')
    return render_template('login.html')

@usuarios_bp.route('/registro', methods=['POST'])
def registro():
    data = {
        'nombre': request.form.get('nombre', '').strip(),
        'apellido': request.form.get('apellido', '').strip(),
        'correo': request.form.get('correo', '').strip().lower(),
        'edad': request.form.get('edad', '').strip(),
        'password': request.form.get('password', ''),
        'confirmar_password': request.form.get('confirmar_password', '')
    }

    if not Usuario.validar_registro(data):
        return redirect('/login/vista')

    if Usuario.correo_existe(data['correo']):
        flash('Este correo ya está registrado.', 'registro')
        return redirect('/login/vista')

    Usuario.crear(data)
    flash('Cuenta creada correctamente. Ahora puedes iniciar sesión.', 'login')
    return redirect('/login/vista')


@usuarios_bp.route('/login', methods=['POST'])
def login():
    correo = request.form.get('correo', '').strip().lower()
    password = request.form.get('password', '')

    usuario = Usuario.buscar_por_correo(correo)

    if not usuario or not Usuario.verificar_password(password, usuario.password):
        flash('Correo o contraseña incorrectos.', 'login')
        return redirect('/login/vista')

    session.clear()
    session['usuario_id'] = usuario.id
    session['nombre'] = usuario.nombre

    return redirect('/entradas')


@usuarios_bp.route('/logout')
def logout():
    session.clear()
    return redirect('/login/vista')
