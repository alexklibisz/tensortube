import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/video', methods=['POST'])
def json_handler():
	data = json.loads(request.data)
	return json.dumps(data)
