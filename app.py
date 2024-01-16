from flask import Flask, request, send_from_directory, jsonify
from generator import SRSGenerator
from os import path
from db import init_app, get_db
from errors.ApiException import ApiException
from models.srs import SrsModel
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor
import json 
  
app = Flask(__name__)
app.config['DATABASE'] = path.join(path.dirname(__file__), 'db.sqlite')
generator = SRSGenerator()
init_app(app)

executor = ThreadPoolExecutor()


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

  executor.submit(generator.generate_and_save_srs_async, body['name'], body['description'])
  
  try: 
    srs = SrsModel.save_to_db(body)
    
    
    return {
      "data": srs,
      "message": "SRS is generating. Please wait a moment."
    }, 201
  except ApiException as e:
    return e.payload, e.status_code

# /api/srs/:id
@app.route('/api/srs/<int:srs_id>', methods=['GET'])
def get_srs_status(srs_id):
    srs_status = generator.get_srs_status(srs_id)
    if srs_status:
        return jsonify(srs_status), 200
    else:
        return 'SRS not found', 404  

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

