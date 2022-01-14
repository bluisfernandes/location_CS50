# from cs50 import SQL
import os
from flask import Flask, request, jsonify, render_template, make_response
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import geojson_rdm_multipoints, geojson_rdm_points, geojson_pointfeature, read_myjson, geojson_featurecollection, featurecollection

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///finance.db")


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
