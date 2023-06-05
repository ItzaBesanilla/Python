from flask import Blueprint, request,jsonify, render_template, url_for, redirect
from sqlalchemy import exc
from models import Usuario
from models import Tarea
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo

appuser = Blueprint('appuser', __name__, template_folder="templates")

@appuser.route('/registro', methods =['POST'])
def registro():
    
    nombreUser = request.form['nombre']
    ApellidoUser = request.form['apellido']
    emailUser= request.form['email']
    userPass = request.form['password']
    searchUser = Usuario.query.filter_by(email=emailUser).first()
    if searchUser:
        mensaje = "El usuario ya existe"
        msj2="Ingrese un nuevo correo electrónico"
    else:
        usuario = Usuario(nombre=nombreUser, apellido=ApellidoUser,email=emailUser, password=userPass)
        try:
            db.session.add(usuario)
            db.session.commit()
            mensaje = "Usuario creado"
            msj2 = "Bienvenido/a"
        except exc.SQLAlchemyError as e:
            mensaje = "Error"
            msj2= ""
    return render_template('MsjRegistro.html', mensaje=mensaje, msj2=msj2, nombre=nombreUser, apellido=ApellidoUser)


@appuser.route('/login', methods=['POST'])
def login():
    
    emailUser = request.form['email']
    userPass = request.form['password']
    searchUser = Usuario.query.filter_by(email=emailUser).first()
    if searchUser:
        validation = bcrypt.check_password_hash(searchUser.password,userPass)
        if validation:
            auth_token = searchUser.encode_auth_token(user_id=searchUser.id)
            print(auth_token)
            if searchUser.admin:
                return redirect(url_for('appuser.vista_admin', auth_token=auth_token))
            else:
                return redirect(url_for('appuser.vista_usuario', auth_token=auth_token))
    return render_template('401.html')


# vista de las funciones del usuario
@appuser.route('/vistaUsuario')
def vista_usuario():
    token = request.args['auth_token']
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    return render_template('indexUsuario.html', token=token, usuario=info_user)


@appuser.route('/vistaAdmin')
def vista_admin():
    token = request.args['auth_token']
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    print(token)
    return render_template('indexAdmin.html', token=token, usuario=info_user)


# Muestra todos los usuarios si recibe un token de usuario admin
@appuser.route('/usuarios') #get
def obtenerUsuarios():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario['data']
    if info_user['admin']:
        output = []
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            usuarioData = {}
            usuarioData['id'] = usuario.id
            usuarioData['email'] = usuario.email
            usuarioData['password'] = usuario.password
            usuarioData['registered_on'] = usuario.registered_on
            usuarioData['admin'] = usuario.admin
            output.append(usuarioData)
    return render_template('ListUsuarios.html', usuarios = output, token = token)