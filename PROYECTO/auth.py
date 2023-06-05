from models import Usuario
from functools import wraps
from flask import request,jsonify


def obtenerInfo(token):
    if token:
        print("TOKEN")
        print (token)
        resp = Usuario.decode_auth_token(token)
        user = Usuario.query.filter_by(id=resp).first()
        if user:
            infoUsuario = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'nombre': user.nombre,
                    'apellido': user.apellido,
                    'email': user.email,
                    'admin': user.admin
                }
            }

            return infoUsuario
        
        else:
            error = {
            'status': 'fail',
            'message': resp
        }
        return error


def tokenCheck(f):
    @wraps(f)
    def verificar(*args,**kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:  
            return jsonify({'message':'token no encontrado'})
        try:
            info= obtenerInfo(token)
            if info['status'] =='fail':
                return jsonify({'message':'token invalido'})
        except:
            return jsonify({'message':'token invalido'})
        return f(info['data'],*args,**kwargs)
    return verificar


def verificarToken(token):
        if not token:  
            return jsonify({'message':'token no encontrado'})
        try:
            info= obtenerInfo(token)
            if info['status'] =='fail':
                return jsonify({'message':'token invalido'})
        except:
            return jsonify({'message':'token invalido'})
        return info