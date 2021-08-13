from flask import Flask, request, jsonify
from flask.typing import TemplateFilterCallable
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
#conexion
app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:43454345@localhost:3306/flaskmysql'
#config para evitar warnings a futuro
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
#pasar configuracion de app al orm
db = SQLAlchemy(app) #instancia SQLAlchemy
ma = Marshmallow(app) #marshmallow para manejar schemma instanciado

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all() # metodo de la instancia db crea nuestras tablas

# crear schemma para interactuar con nuestras tablas
class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description')

# ahora instanciamos taskschema

task_schema = TaskSchema() #task_schema instancia de TaskSchema() para una sola tarea
tasks_schema = TaskSchema(many=True) #task_schema instancia de TaskSchema() para varias tareas

# end points de esta app

@app.route('/tasks', methods=['POST']) # ruta crear datos
def create_task():
    #print(request.json)
    #return 'received'
    title = request.json['title']
    description = request.json['description']
    new_task = Task(title, description) #he creado una nueva tarea
    db.session.add(new_task)
    db.session.commit()

    return task_schema.jsonify(new_task) #respondemos al cliente para que vea lo que ha creado

@app.route('/tasks',methods=['GET']) # ruta obtener datos para mostrar al cliente
def get_tasks():
    all_tasks = Task.query.all() # devuelve todas las tareas
    results = tasks_schema.dump(all_tasks) # devuelve lista de tareas para el cliente
    return jsonify(results) # conversion string a json

@app.route('/tasks/<id>',methods=['GET']) # devuelve las tareas segun el id
def get_task(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT']) # actualizar tarea
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']

    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"pequeña API de prueba"})

if __name__ == '__main__':
    app.run(debug=True)








