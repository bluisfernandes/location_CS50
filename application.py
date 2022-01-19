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
jsonlocation = {}
featurecollection

@app.route("/")
def index():
  	return render_template("index.html", title="location cs50")
  	
  	
@app.route("/how")
def how():
  	return render_template("how.html", title="how")
  	
  	
@app.route("/device")
def device():
  	return render_template("device.html", title="device")
  	

@app.route("/custom_map")
def custom():
  	return render_template("map_custom.html", title="admin")
  	
  	
@app.route("/admin")
def admin():
  	return render_template("admin.html", title="admin")


@app.route("/mappoints", methods=['GET'])
def map_points():
	npoints = int(request.args.get('n'))
	geojson = geojson_rdm_points(npoints)
	return render_template("blank.html", title ="mappoints", geojson = geojson)


@app.route("/inputapplocation", methods=['POST', 'GET'])
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
		return render_template("blank.html", title ="input app location", geojson = jsonlocation)
	else:
		return render_template("inputapplocation.html")

	
@app.route("/lastmap", methods=['GET'])
def map_last_map():
	global featurecollection
	return render_template("blank.html", title ="lastmap", geojson = featurecollection)


@app.route('/checkjson', methods=['POST', 'GET'])
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

	return render_template("locatioch.html")


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

	features = geojson_pointfeature(points)

	featurecollection_geral = geojson_featurecollection(features)
	# print(featurecollection_geral)
	return render_template("blank.html", title = "geral", geojson = featurecollection_geral)


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
