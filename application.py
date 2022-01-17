from cs50 import SQL
import os
from flask import Flask, request, jsonify, render_template, make_response
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import geojson_rdm_multipoints, geojson_rdm_points, geojson_pointfeature
from helpers import read_myjson, geojson_featurecollection, featurecollection, store_data

# Configure application
app = Flask(__name__)



# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///location.db")


# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")

n = 1000
npoints = 1000
jsonlocation = {}
featurecollection

@app.route("/")
def index():
  	return '''
		Its working!<br><br>

		<a href="/location">/location<a><br>
		<a href="/postjson">/postjson<a><br>
		<a href="/maptest?n=1000">/maptest?n=1000<a><br>
		<a href="/mappoints?n=2500">/mappoints?n=2500<a><br>
		<a href="/lastmap">/lastmap<a><br>
		<a href="/geral">/geral<a><br>
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
	print(geojson)
	return render_template("script_points.js", geojson = geojson)


@app.route("/script_lastmap.js")
def script_lastmaps():
	global featurecollection
	return render_template("script_lastmap.js", geojson = featurecollection)


@app.route("/script_geral.js")
def script_geral():
	global featurecollection_geral
	return render_template("script_lastmap.js", geojson = featurecollection_geral)


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
		json_app = request.get_json()

		if isinstance(json_app, dict):
			# save poinsts from app in a file and SQL
			code, message = store_route(json_app)
			res = make_response(jsonify(message), code)
			print(f"__response {code}")

		else:
			formato = f"must be JSON, its a {type(json_app)}"
			res = make_response(jsonify({"message": formato}), 405)
			print(f"__Response error: {formato}")

		# print(type(res.get_json()))

		return res

	return '''Try to post a JSON<br>
					Example in <a href=https://colab.research.google.com/drive/1H-cBSzQcHqKl-CObhL1_tl76_76lynNX?usp=sharing>Colab<a>.'''


@app.route("/geral")
def geral():
	sql = db.execute("SELECT * FROM location")

	points=[]
	# [[long, lat, sensor, timestamp, user],]
	for i in range(len(sql)):
		points.append([sql[i]["long"], sql[i]["lat"] ,sql[i]["sensor"] ,sql[i]["timestamp"] ,sql[i]["user"] ])
	# sql_mode = db.execute(".mode list")

	features = geojson_pointfeature(points)

	global featurecollection_geral
	featurecollection_geral = geojson_featurecollection(features)
	# print(featurecollection_geral)
	return render_template("map_test1.html", site_map=True, geojson = featurecollection_geral, script_src = 'script_geral.js')


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
	# save in Database SQL
	print(store_data(points))

	# transform on a json
	features = geojson_pointfeature(points)
	global featurecollection
	featurecollection = geojson_featurecollection(features)

	# res = {"timestamp":json["info"][0]["timestamp"], "size":len(json["points"])}
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
