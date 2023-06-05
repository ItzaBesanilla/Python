from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from flask_migrate import Migrate
from config import BasicConfig
from database import db
from encriptador import bcrypt
from routes.usuario.usuario import appuser
from routes.tarea.tarea import apptask

import logging

app = Flask(__name__)

app.register_blueprint(appuser)
app.register_blueprint(apptask)
app.config.from_object(BasicConfig)
db.init_app(app)
CORS(app)

bcrypt.init_app(app)
migrate = Migrate()
migrate.init_app(app, db)
logging.basicConfig(level=logging.DEBUG, filename='debug.log') 

@app.route('/VerTareasAdmin')
def ver_Tarea_Admin():
    return render_template('IndexAdmin.html')


@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def iniciar_sesion():
    return render_template('login.html')

def pagina_no_encontrada(error):
    return render_template('404.html')


app.register_error_handler(404, pagina_no_encontrada)


def peticion_incorrecta(error):
    return render_template('400.html')


app.register_error_handler(400, peticion_incorrecta)