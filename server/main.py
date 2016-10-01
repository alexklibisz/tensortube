import json
from flask import Flask, request, redirect, url_for, send_from_directory
import downloader

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
    reqData = json.loads(request.data)
    # frames = downloader.extract_files(reqData['url'])

    # Response data should be formatted like this.
    resData = {
        "labels": [
            {
                "name": "cat",
                "times": [40,50,60,70]
            },
            {
                "name": "dog",
                "times": [120,130,140]
            }
        ]
    }
    print(resData)
    return(json.dumps(resData))

if __name__ == '__main__':
  app.run()
