from flask import Flask, request, send_from_directory
from generator import SRSGenerator
from os import path
from db import init_app, get_db
from errors.ApiException import ApiException
from models.srs import SrsModel
import json
  
app = Flask(__name__)
app.config['DATABASE'] = path.join(path.dirname(__file__), 'db.sqlite')

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

  generator = SRSGenerator(body)

  # generator.generate()

  try: 
    srs = SrsModel.save_to_db(body)
    return {
      "data": srs,
      "message": "SRS is generating. Please wait a moment."
    }, 201
  except ApiException as e:
    return e.payload, e.status_code

# /api/srs/:id
  
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

