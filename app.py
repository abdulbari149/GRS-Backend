from flask import Flask, request, send_from_directory
from generator import SRSGenerator
from os import path

  
app = Flask(__name__)

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

  if not body_validation(body, ['name', 'description', 'style']):
    return 'Missing fields', 400

  generator = SRSGenerator(body)

  return generator.generate(), 200
  

@app.route('/documents/<path:filename>')
def staticfiles(filename):
    return send_from_directory('./assets/documents', filename)

if __name__ == '__main__':
  app.run(debug=True)