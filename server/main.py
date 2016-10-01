#!/usr/bin/env python2.7
from __future__ import print_function
import json
from flask import Flask, request, redirect, url_for, send_from_directory
import downloader
import classifier
import cv2

# Setup Flask app.
app = Flask(__name__)
app.debug = True
app._static_folder = '../client'


# Setup classifier.
# Creates classification network and node ID --> English string lookup.
node_lookup = classifier.NodeLookup()

# Routes
@app.route('/')
def root():
  return app.send_static_file('index.html')

@app.route('/<path:path>')
def static_proxy(path):
  return app.send_static_file(path)

@app.route('/video', methods=['POST'])
def json_handler():

    classifier.create_graph()
    reqData = json.loads(request.data)
    print (reqData['url'])
    frames = downloader.extract_files(reqData['url'])
    print ("%d frames" % (len(frames)))
    for t, f in enumerate(frames):
        if t > 5:
            break
        img_str = cv2.imencode('.jpg', f)[1].tostring()
        top_predictions, all_predictions = classifier.get_top_predictions_jpg_data(img_str, 1)

        for node_id in top_predictions:
            human_string = node_lookup.id_to_string(node_id)
            score = all_predictions[node_id]
            print('frame %d %s (score = %.5f)' % (t, human_string, score))

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
