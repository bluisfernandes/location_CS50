# from cs50 import SQL
import os
from flask import Flask, request, jsonify, render_template, make_response
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import geojson_rdm_multipoints, geojson_rdm_points, geojson_pointfeature, read_myjson, geojson_featurecollection

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

n = 1000
npoints = 1000
jsonlocation = {}
featurecollection ={"features": [{"geometry": {"coordinates": [-70.60013, -33.416747], "type": "Point"}, "properties": {"color": 18443, "time": "2022-01-11T15:25:27.309"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600188, -33.416757], "type": "Point"}, "properties": {"color": 638, "time": "2022-01-11T15:25:32.765"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600262, -33.416718], "type": "Point"}, "properties": {"color": 2403, "time": "2022-01-11T15:25:33.772"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600313, -33.41674], "type": "Point"}, "properties": {"color": 297, "time": "2022-01-11T15:25:36.496"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60038, -33.41673], "type": "Point"}, "properties": {"color": 993, "time": "2022-01-11T15:25:45.505"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60042, -33.416695], "type": "Point"}, "properties": {"color": 701, "time": "2022-01-11T15:25:49.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600487, -33.416687], "type": "Point"}, "properties": {"color": 467, "time": "2022-01-11T15:25:55.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600553, -33.416693], "type": "Point"}, "properties": {"color": 257, "time": "2022-01-11T15:25:59.507"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60061, -33.416717], "type": "Point"}, "properties": {"color": 272, "time": "2022-01-11T15:26:03.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600667, -33.416745], "type": "Point"}, "properties": {"color": 9342, "time": "2022-01-11T15:26:06.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600732, -33.41676], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:10.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600793, -33.416777], "type": "Point"}, "properties": {"color": 372, "time": "2022-01-11T15:26:13.483"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600847, -33.416787], "type": "Point"}, "properties": {"color": 182, "time": "2022-01-11T15:26:16.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600903, -33.4168], "type": "Point"}, "properties": {"color": 2047, "time": "2022-01-11T15:26:20.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.600945, -33.41684], "type": "Point"}, "properties": {"color": 667, "time": "2022-01-11T15:26:24.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601, -33.416863], "type": "Point"}, "properties": {"color": 661, "time": "2022-01-11T15:26:28.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60107, -33.416878], "type": "Point"}, "properties": {"color": 2587, "time": "2022-01-11T15:26:35.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601135, -33.416893], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:40.496"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601197, -33.416892], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:44.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601255, -33.416892], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:47.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601315, -33.4169], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:51.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601377, -33.416902], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:26:56.522"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60143, -33.416933], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:00.524"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601493, -33.416935], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:03.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601542, -33.416957], "type": "Point"}, "properties": {"color": 529, "time": "2022-01-11T15:27:06.520"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601592, -33.416975], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:09.516"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601648, -33.416987], "type": "Point"}, "properties": {"color": 2227, "time": "2022-01-11T15:27:14.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601712, -33.417005], "type": "Point"}, "properties": {"color": 9071, "time": "2022-01-11T15:27:18.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601768, -33.41701], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:21.521"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60183, -33.417003], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:25.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601885, -33.416968], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:29.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601943, -33.41697], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:33.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.601997, -33.416963], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:38.520"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602048, -33.416923], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:42.487"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602093, -33.416893], "type": "Point"}, "properties": {"color": 9566, "time": "2022-01-11T15:27:45.505"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602128, -33.416857], "type": "Point"}, "properties": {"color": 722, "time": "2022-01-11T15:27:48.504"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602175, -33.41682], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:52.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602227, -33.416798], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:55.479"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602278, -33.416775], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:27:58.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602335, -33.416753], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:01.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602385, -33.41673], "type": "Point"}, "properties": {"color": 717, "time": "2022-01-11T15:28:05.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602438, -33.4167], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:10.540"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602487, -33.416663], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:14.483"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602535, -33.416628], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:18.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602585, -33.41661], "type": "Point"}, "properties": {"color": 10330, "time": "2022-01-11T15:28:22.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60265, -33.416598], "type": "Point"}, "properties": {"color": 2156, "time": "2022-01-11T15:28:26.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602708, -33.416592], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:30.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602762, -33.416565], "type": "Point"}, "properties": {"color": 2629, "time": "2022-01-11T15:28:35.494"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60281, -33.41654], "type": "Point"}, "properties": {"color": 796, "time": "2022-01-11T15:28:38.537"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602863, -33.416523], "type": "Point"}, "properties": {"color": 682, "time": "2022-01-11T15:28:41.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.602932, -33.41652], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:28:44.535"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603005, -33.416518], "type": "Point"}, "properties": {"color": 10830, "time": "2022-01-11T15:28:47.476"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603073, -33.416513], "type": "Point"}, "properties": {"color": 702, "time": "2022-01-11T15:28:50.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603133, -33.416505], "type": "Point"}, "properties": {"color": 579, "time": "2022-01-11T15:28:53.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603188, -33.416488], "type": "Point"}, "properties": {"color": 2253, "time": "2022-01-11T15:28:56.492"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603243, -33.416475], "type": "Point"}, "properties": {"color": 741, "time": "2022-01-11T15:28:59.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603305, -33.416453], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:02.542"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60337, -33.416433], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:05.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603423, -33.416418], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:08.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603478, -33.41641], "type": "Point"}, "properties": {"color": 669, "time": "2022-01-11T15:29:12.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603543, -33.4164], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:18.523"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603577, -33.416363], "type": "Point"}, "properties": {"color": 642, "time": "2022-01-11T15:29:22.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603633, -33.416343], "type": "Point"}, "properties": {"color": 540, "time": "2022-01-11T15:29:26.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60369, -33.416323], "type": "Point"}, "properties": {"color": 2158, "time": "2022-01-11T15:29:30.525"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603748, -33.416305], "type": "Point"}, "properties": {"color": 615, "time": "2022-01-11T15:29:33.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603803, -33.416275], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:37.526"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603875, -33.416268], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:41.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603937, -33.416248], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:45.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.603993, -33.41627], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:29:50.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60404, -33.416303], "type": "Point"}, "properties": {"color": 11669, "time": "2022-01-11T15:29:55.493"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604095, -33.41632], "type": "Point"}, "properties": {"color": 732, "time": "2022-01-11T15:30:00.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604147, -33.416305], "type": "Point"}, "properties": {"color": 588, "time": "2022-01-11T15:30:10.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604197, -33.41634], "type": "Point"}, "properties": {"color": 2362, "time": "2022-01-11T15:30:17.506"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60423, -33.416377], "type": "Point"}, "properties": {"color": 724, "time": "2022-01-11T15:30:22.513"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604282, -33.41642], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:27.534"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60432, -33.416452], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:30.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604363, -33.416492], "type": "Point"}, "properties": {"color": 10934, "time": "2022-01-11T15:30:35.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604402, -33.416542], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:39.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604432, -33.416592], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:43.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604467, -33.416627], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:46.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.6045, -33.416673], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:50.526"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604543, -33.416718], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:55.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604577, -33.416767], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:30:59.527"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604612, -33.416803], "type": "Point"}, "properties": {"color": 506, "time": "2022-01-11T15:31:03.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604673, -33.416833], "type": "Point"}, "properties": {"color": 579, "time": "2022-01-11T15:31:07.522"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604733, -33.416863], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:31:12.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604763, -33.416902], "type": "Point"}, "properties": {"color": 18443, "time": "2022-01-11T15:31:16.533"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60482, -33.416895], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:32:28.515"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604872, -33.416882], "type": "Point"}, "properties": {"color": 10497, "time": "2022-01-11T15:32:31.519"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604925, -33.416905], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:32:54.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60495, -33.416948], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:32:57.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.604982, -33.417], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:01.536"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605017, -33.417047], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:05.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605052, -33.417097], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:09.535"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605085, -33.417148], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:13.532"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605123, -33.417193], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:17.531"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605145, -33.417247], "type": "Point"}, "properties": {"color": 18443, "time": "2022-01-11T15:33:21.499"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605173, -33.417292], "type": "Point"}, "properties": {"color": 12294, "time": "2022-01-11T15:33:25.529"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605197, -33.417342], "type": "Point"}, "properties": {"color": 9587, "time": "2022-01-11T15:33:30.528"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605217, -33.417387], "type": "Point"}, "properties": {"color": 515, "time": "2022-01-11T15:33:34.524"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.60524, -33.417433], "type": "Point"}, "properties": {"color": 620, "time": "2022-01-11T15:33:39.530"}, "type": "Feature"}, {"geometry": {"coordinates": [-70.605258, -33.417478], "type": "Point"}, "properties": {"color": 259, "time": "2022-01-11T15:33:45.532"}, "type": "Feature"}], "type": "FeatureCollection"}

@app.route("/")
def index():
  	return '''
		Its working!<br><br>

		<a href="/location">/location<a><br>
		<a href="/postjson">/postjson<a><br>
		<a href="/maptest?n=1000">/maptest?n=1000<a><br>
		<a href="/mappoints?n=5000">/mappoints?n=5000<a><br>
		'''


# TODO: redirect if there isnt a arg
@app.route("/maptest", methods=['GET'])
def map_test():
	global n
	n = int(request.args.get('n'))
	geojson = geojson_rdm_multipoints(n)
	return render_template("map_test.html", site_map=True, geojson = geojson)


@app.route("/mappoints", methods=['GET'])
def map_points():
	global npoints
	npoints = int(request.args.get('n'))
	geojson = geojson_rdm_points(npoints)
	return render_template("map_test1.html", site_map=True, geojson = geojson, script_src = 'script_points.js')


@app.route("/maplocation", methods=['POST', 'GET'])
def map_location():
	global jsonlocation
	if request.method == "POST":
		a = request.form.get("json")
		try:
			jsonlocation = json.loads(a)
			if isinstance(jsonlocation, dict):
				pass
			else:
				res = make_response(jsonify({"message": "must be JSON, its probably numeric"}), 405)
		except:
			return make_response(jsonify({"message": "must be JSON, its probably a string"}), 405)
		# return res
		print(f'the type of geojson here is {type(jsonlocation)}.')
		return render_template("map_test1.html", site_map=True, geojson = jsonlocation, script_src = 'script_location.js')
	else:
		return render_template("maplocation.html")


	
@app.route("/lastmap", methods=['GET'])
def map_last_map():
	global featurecollection
	return render_template("map_test1.html", site_map=True, geojson = featurecollection, script_src = 'script_lastmap.js')


@app.route("/script.js")
def script():
	geojson = geojson_rdm_multipoints(n)
	return render_template("script.js", geojson = geojson)


@app.route("/script_points.js")
def script_points():
	geojson = geojson_rdm_points(npoints)
	return render_template("script_points.js", geojson = geojson)


@app.route("/script_lastmap.js")
def script_lastmaps():
	global featurecollection
	return render_template("script_points.js", geojson = featurecollection)


@app.route("/script_location.js")
def script_location():
	global jsonlocation
	return render_template("script_points.js", geojson = jsonlocation)


@app.route('/location', methods=['POST', 'GET'])
def location():
	if request.method == "POST":
		a = request.form.get("username")
		try:
			b = json.loads(a)
			if isinstance(b, dict):
				res = make_response(jsonify(b), 200)
			else:
				res = make_response(jsonify({"message": "must be JSON, its probably numeric"}), 405)

		except:
			return make_response(jsonify({"message": "must be JSON, its probably a string"}), 405)

		return res

	return render_template("location.html")


# Used to communicate with Android APP or colab
@app.route('/postjson', methods=['POST', 'GET'])
def postjson():
	if request.method == "POST":
		a = request.get_json()

		if isinstance(a, dict):
			code, message = store_route(a)
			res = make_response(jsonify(message), code)
			print(f"__response {code}")

		else:
			formato = f"must be JSON, its a {type(a)}"
			res = make_response(jsonify({"message": formato}), 405)
			print(f"__Response error: {formato}")

		# print(type(res.get_json()))

		return res

	return '''Try to post a JSON<br>
					Example in <a href=https://colab.research.google.com/drive/1H-cBSzQcHqKl-CObhL1_tl76_76lynNX?usp=sharing>Colab<a>.'''


def store_route(json_request):

	# check if there are all keys
	try:
		print("_______________________________")
		print(json_request["id"])
		print("______________")
		print(json_request["device"])
		print("______________")
		print(json_request["points"][0])
		print("______________")
		print(json_request["info"][0])
	except:

		# return code of error and expected json
		return 403, {"message":"some parameters are missing","expected":{"id": 10, "device": "xxx", "points":[{"lat": 123.456, "long": 987.654 },{"lat": 123.457, "long": 987.655 }],"info":[{"point_id":0,"route_id":0,"sensor_light":13333.3,"timestamp":"2022-01-11T00:59:53.372"},{"point_id":1,"route_id":0,"sensor_light":13345.9,"timestamp":"2022-01-11T00:59:54.926"}]}}


	path = f'/home/runner/locationcs50/storage/{json_request["device"]}'

	if not os.path.exists(path):
			os.makedirs(path)

	name = json_request['info'][0]['timestamp']+"_"+str(len(json_request["points"]))

	with open(f'{path}/{name}.txt', 'w') as file:
			file.write(str(json_request))


	#converts a json from app to a geojson
	points = read_myjson(json_request)
	features = geojson_pointfeature(points)
	global featurecollection
	featurecollection = geojson_featurecollection(features)


	# store_id = 0
	# json_request["device"]
	# json_request["id"]
	# json_request["info"][0]["timestamp"]

	# json_request["points"]
	# json_request["info"]

# TODO: store values on sqlite
# user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
# db.execute("INSERT INTO wallet(user_id, symbol, shares, user_id_symbol) VALUES (?, ?, ?, ?)",
                      #  session['user_id'], stock['symbol'], shares, user_id_symbol)
# db.execute("UPDATE wallet SET shares = ? WHERE user_id_symbol = ? ", shares, user_id_symbol)

	return 200, json_request


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

def apology(msg, code=400):
	msg_site = "ERROR! name: " +msg + " code: " + str(code)
	return render_template("blank.html", title = f"erro: {code}", content = msg_site)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


app.run(host='0.0.0.0', port=5000, debug=False) # Run the Application
