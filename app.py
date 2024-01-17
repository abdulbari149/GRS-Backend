from flask import Flask, request, send_from_directory, jsonify
from generator import SRSGenerator, create_task
from os import path
from db import init_app, get_db
from errors.ApiException import ApiException
from models.srs import SrsModel
from celery_config import celery_app
from celery.result import AsyncResult
  
app = Flask(__name__)
app.config['DATABASE'] = path.join(path.dirname(__file__), 'db.sqlite')
celery_app.conf.update(app.config)
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
  body = request.get_json()


  if not body_validation(body, ['name', 'description']):
    return 'Missing fields', 400
  
  task = create_task.apply_async(args=(generator,body))
  body['task_id'] = task.id
  
  try: 
    srs = SrsModel.save_to_db(body)
    
    
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

@app.get("/api/srs/<int:id>/result")
def task_result(id: str) -> dict[str, object]:
  try:
    srs = SrsModel.get_by_id(id)
    result = AsyncResult(id = srs['task_id'])
    return {
        "ready": result.ready(),
        "successful": result.successful(),
        "value": result.result if result.ready() else None,
    }  
  except ApiException as e:
    return e.payload, e.status_code 
    
    


@app.route('/documents/<path:filename>')
def staticfiles(filename):
    return send_from_directory('./assets/documents', filename)

