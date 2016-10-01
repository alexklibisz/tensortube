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
videoFolder = './server/videos'

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

    filename = videoFolder + "/" + downloader.get_youtube_id(reqData['url']) + ".json"
    print (filename) #filename = "./server/videos/YbcxU1IK7s4.json"
    try:
        cached = open(filename, 'r')
        print("Found %s in JSON cache" % (filename))
        return cached.read()
    except:
        print("Didn't find %s in JSON cache" % (filename))
        pass

    print (reqData['url'])
    frames = downloader.extract_files(reqData['url'])
    print ("%d frame%s" % (len(frames), 's' if len(frames) > 1 else ''))

    resData = {"labels" : {}}
    # Add important frames to resData
    for t, f in enumerate(frames):
        img_str = cv2.imencode('.jpg', f)[1].tostring()
        top_predictions, all_predictions = classifier.get_top_predictions_jpg_data(img_str, 1)

        for node_id in top_predictions:
            human_string = node_lookup.id_to_string(node_id)
            score = all_predictions[node_id]

            # Add to response data if above a certain threshold
            if score > 0.4:
                if human_string not in resData["labels"]:
                    resData["labels"][human_string] = {"times" : []}
                resData["labels"][human_string]["times"].append(t)
            print('frame %d %s (score = %.5f)' % (t, human_string, score))
    
    # Response data should be formatted like this.
    # resData = {
    #     "labels": {
    #         "cat" : {
    #             "times": [40,50,60,70],
    #             "scores" : [0.8, 0.3, 0.4, 0.9]
    #         },
    #         "dog" : {
    #             "times": [120,130,140]
    #             "scores" : [0.8, 0.3, 0.4]
    #         }
    #     }
    # }


    # Remove any consecutive label times
    for label, obj in resData["labels"].items():
        start = 1
        times = obj["times"]
        for i in range(1, len(times), 1):
            if times[i] - times[i-1] > 1:
                times[start] = times[i]
                start = start + 1
        obj["times"] = times[:start]

    print(resData)
    resJson = json.dumps(resData)
    cached = open(filename, 'w')
    cached.write(resJson)
    return resJson



if __name__ == '__main__':
  app.run()
