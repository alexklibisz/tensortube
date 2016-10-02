#!/usr/bin/env python2.7
from __future__ import print_function
import json
from flask import Flask, request, redirect, url_for, send_from_directory
import downloader
import classifier
import cv2
import numpy as np
import sys
import os
import glob

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


@app.route('/cached', methods=['GET'])
def cached_handler():
    resData = []
    for file in glob.glob(videoFolder + "/*.json"):
        resData.append(file.rsplit('.', 1)[0].rsplit('/', 1)[-1])
    return json.dumps(resData)

@app.route('/video', methods=['POST'])
def json_handler():

    classifier.create_graph()
    reqData = json.loads(request.data)
    youtube_id = downloader.get_youtube_id(reqData['url'])
    filename = videoFolder + "/" + youtube_id + ".json"
    print (filename)
    try:
        cached = open(filename, 'r')
        print("Found %s in JSON cache" % (filename))
        resJson = cached.read()
        # print (resJson)
        resData = json.loads(resJson)
    except:
        print("Didn't find %s in JSON cache: %s" % (filename, str(sys.exc_info())) )
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
                score = np.asscalar(all_predictions[node_id])

                # Add to response data if above a certain threshold
                if human_string not in resData["labels"]:
                    resData["labels"][human_string] = {"times" : [], 
                                                        "scores" : [],
                                                        "labelId" : node_lookup.string_to_id(human_string)}
                resData["labels"][human_string]["times"].append(t)
                resData["labels"][human_string]["scores"].append(score)
                print('frame %d %s (score = %.5f)' % (t, human_string, score))
        
        # Response data should be formatted like this.
        # resData = {
        #     "labels": {
        #         "cat" : {
        #             "labelId" : "n02121620",
        #             "times": [40,50,60,70],
        #             "scores" : [0.8, 0.3, 0.4, 0.9]
        #         },
        #         "dog" : {
        #             "labelId" : "n03218446",
        #             "times": [120,130,140]
        #             "scores" : [0.8, 0.3, 0.4]
        #         }
        #     }
        # }


        # Remove any consecutive label times
        for label, obj in resData["labels"].items():
            start = 1
            times = obj["times"]
            scores = obj["scores"]
            for i in range(1, len(times), 1):
                if times[i] - times[i-1] > 1:
                    times[start] = times[i]
                    scores[start] = scores[i]
                    start = start + 1
                else:
                    # stick the higher value into the one we're keeping for this label
                    if scores[i] > scores[start-1]:
                        scores[start-1] = scores[i]
            obj["times"] = times[:start]
            obj["scores"] = scores[:start]

        print(resData)
        resJson = json.dumps(resData)
        cached = open(filename, 'w')
        cached.write(resJson)
    else:
        # See if this cached file has the labelId attribute
        for label, info in resData["labels"].items():
            good = ("labelId" in info) and isinstance(info["labelId"], basestring)
            break
        if not good:
            for label, info in resData["labels"].items():
                info["labelId"] = node_lookup.string_to_id(label)
                info["youtubeId"] = youtube_id
            # Write to cache
            print("Adding nodeIds to cached data")
            print(resData)
            resJson = json.dumps(resData)
            cached = open(filename, 'w')
            cached.write(resJson)
    pruneLabels(resData, 0.4)
    return json.dumps(resData)

# Removes all entries with a score lower than the the given threshold
def pruneLabels(resData, threshold):
    for label, obj in resData["labels"].items():
        start = 0
        times = obj["times"]
        scores = obj["scores"]
        for i in range(len(times)):
            if scores[i] >= threshold:
                times[start] = times[i]
                scores[start] = scores[i]
                start = start + 1
        obj["times"] = times[:start]
        obj["scores"] = scores[:start]
        if len(obj["times"]) == 0:
            del resData["labels"][label]

    resData["sortedLabels"] = sorted(resData["labels"], key=lambda label: max(resData["labels"][label]["scores"]), reverse=True)

if __name__ == '__main__':
  app.run()
