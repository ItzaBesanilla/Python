import datetime
import jwt
from app import db, bcrypt
from config import BasicConfig


class Usuario(db.Model):
    __tablename__ = "Usuario"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido =db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    

    def __init__(self, nombre, apellido, email, password, admin=False):
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, BasicConfig.BCRYPT_LOG_ROUNDS
        ).decode()
        self.admin = admin

    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp':datetime.datetime.utcnow()+datetime.timedelta(days=1,hours=10),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                BasicConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload=jwt.decode(
                auth_token,
                BasicConfig.SECRET_KEY,
                algorithms=["HS256"]
            )
            return payload['sub']
        except jwt.ExpiredSignatureError as e:
            print(e)
            return "token expirado"
        except jwt.InvalidTokenError as e:
            return "token invalido"

class Tarea(db.Model):
    __tablename__ = "Tarea"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.String(50), nullable=False)
    fecha = db.Column(db.Date, nullable=False, default=None)
    estado = db.Column(db.Boolean, nullable=False, default=True)
    
    def __init__(self, titulo, descripcion, fecha, estado = False):
        self.titulo = titulo
        self.descripcion=descripcion
        self.fecha = fecha
        self.estado=estado
        
    def __str__(self):
        return f'ID: {self.id}, Titulo:{self.titulo}, Descripcion:{self.descripcion}, Fecha: {self.fecha}, Estado: {self.estado}'

                
