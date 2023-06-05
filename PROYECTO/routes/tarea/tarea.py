from flask import Blueprint, request,jsonify, render_template, url_for, redirect, g
from sqlalchemy import exc
from models import Tarea
from models import Usuario
from app import db,bcrypt
from auth import tokenCheck, obtenerInfo
from datetime import date
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

apptask = Blueprint('apptask', __name__, template_folder="templates")

# @apptask.route('/form/agregar')
# def formulario_registrar():
#     token = request.args.get('token')
#     return render_template('Agregar.html', token=token)


@apptask.route('/agregarTarea', methods=['GET','POST'])
def agregar_tarea():
    token = request.args.get('token')
    usuario = obtenerInfo(token)

    if request.method == 'POST':
      tituloT = request.form['titulo']
      descT = request.form['descripcion']
      fechaT = request.form['fecha']
      tarea = Tarea(titulo=tituloT, descripcion=descT, fecha=fechaT)
      db.session.add(tarea)
      db.session.commit()
      
      return redirect(url_for('apptask.ver_Tareas_admin', token=token))
    return render_template('indexAdmin.html', token=token, usuario=usuario)



@apptask.route('/VerTareas')
def ver_Tareas():
    token = request.args.get('token')
    usuario = obtenerInfo(token)
    info_user = usuario.get('data')
    tareas = Tarea.query.order_by(Tarea.fecha.asc()).all()
    
    if tareas:
        output = []
        for tarea in tareas:
            tareaData = {}
            tareaData['id'] = tarea.id
            tareaData['titulo'] = tarea.titulo
            tareaData['descripcion'] = tarea.descripcion
            tareaData['fecha'] = tarea.fecha
            tareaData['estado'] = tarea.estado
            output.append(tareaData)
    else:
        output = []

    return render_template('indexUsuario.html', tareas=output, token=token, usuario=info_user)

@apptask.route('/VerTareasAdmin')
def ver_Tareas_admin():
    token = request.args.get('token')
    tareas = Tarea.query.order_by(Tarea.fecha.asc()).all()
    
    if tareas:
        output = []
        for tarea in tareas:
            tareaData = {}
            tareaData['id'] = tarea.id
            tareaData['titulo'] = tarea.titulo
            tareaData['descripcion'] = tarea.descripcion
            tareaData['fecha'] = tarea.fecha
            tareaData['estado'] = tarea.estado
            output.append(tareaData)
    else:
        output = []

    return render_template('indexAdmin.html', tareas=output, token=token)
    



@apptask.route('/eliminarTarea', methods=["POST"]) 
def eliminar_Tarea():
    token = request.args.get('token')
    tarea_id = request.form['id']
    tarea = Tarea.query.filter_by(id=tarea_id).first()
    output = []
    if tarea:
        db.session.delete(tarea)
        db.session.commit()
        mensaje = "Tarea eliminada"
    
    tareas = Tarea.query.all()
    for tarea in tareas:
        tareaData = {}
        tareaData['id'] = tarea.id
        tareaData['titulo'] = tarea.titulo
        tareaData['descripcion'] = tarea.descripcion
        tareaData['fecha'] = tarea.fecha
        tareaData['estado'] = tarea.estado
        output.append(tareaData)
    
    return render_template('IndexAdmin.html', tareas=output, token=token)

