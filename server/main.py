import json
from flask import Flask, request, redirect, url_for, send_from_directory

# Setup Flask app.
app = Flask(__name__)
app.debug = True
app._static_folder = '../client'

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/video', methods=['POST'])
def json_handler():
	data = json.loads(request.data)
	return json.dumps(data)

if __name__ == '__main__':
  app.run()
