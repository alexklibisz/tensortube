import json
from flask import Flask, request, redirect, url_for, send_from_directory
import downloader
import classifier

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
	# Creates classification network and node ID --> English string lookup.
	classifier.create_graph()
	node_lookup = classifier.NodeLookup()

	reqData = json.loads(request.data)
	frames = downloader.extract_files(reqData['url'])
	i = 0
	print (len(frames))
	for f in frames:
		img_str = cv2.imencode('.jpg', f)[1].tostring()
		top_predictions, all_predictions = classifier.get_top_predictions_jpg_data(img_str, 1)

		for node_id in top_predictions:
			human_string = node_lookup.id_to_string(node_id)
			score = all_predictions[node_id]
			print('frame %d %s (score = %.5f)' % (i, human_string, score))
		i = i + 1
	return json.dumps(reqData)


if __name__ == '__main__':
  app.run()
