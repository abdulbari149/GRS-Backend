from db import init_app, get_db
from errors.ApiException import ApiException
from models.srs import SrsModel

from flask import Flask, request, send_from_directory
from os import path
from generator import SRSGenerator, SrsModel
import threading
import atexit
# from flask_ngrok import run_with_ngrok

bg_thread = None

app = Flask(__name__)
#run_with_ngrok(app)
app.config['DATABASE'] = path.join(path.dirname(__file__), 'db.sqlite')

generator = SRSGenerator()

init_app(app)


@app.route('/')
def hello_world():
    return 'Hello, World!'


def body_validation(body, fields):
    for field in fields:
        if field not in body:
            return False
    return True


# body = { name, description }

@app.route('/api/generate', methods=['POST'])
def generate():
    global bg_thread
    body = request.get_json()

    if not body_validation(body, ['name', 'description']):
        return 'Missing fields', 400
    
    if bg_thread and bg_thread.is_alive():
        print("Stopping previous background thread...")
        bg_thread.deamon()

    try:
        print("Starting new background thread...")
        database = get_db()
        
        body['task_id'] = 'task.id'
        srs = SrsModel.save_to_db(body)
        
        bg_thread = threading.Thread(target=generator.generate_srs, args=(srs, database))
        bg_thread.start()
        
    
        return {
            "data": srs,
            "message": "SRS is generating. Please wait a moment."
        }, 201
    except ApiException as e:
        return e.payload, e.status_code

@app.route('/api/srs/<int:id>', methods=['GET'])
def get_srs(id):
    try:
        srs = SrsModel.get_by_id(id)
        return {
            "data": srs,
            "message": "SRS is generating. Please wait a moment."
        }, 200
    except ApiException as e:
        return e.payload, e.status_code


@app.route('/documents/<path:filename>')
def staticfiles(filename):
    return send_from_directory('./assets/documents', filename)

# Register a function to stop the thread when the application exits
def stop_background_task():
    print("CleanUp ... Stopping background thread...")
    if bg_thread and bg_thread.is_alive():
        bg_thread.deamon()
atexit.register(stop_background_task)
