from cs50 import SQL
import os
from flask import Flask, request, jsonify, render_template, make_response
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import geojson_rdm_multipoints, geojson_rdm_points, geojson_pointfeature
from helpers import read_myjson, geojson_featurecollection, featurecollection, store_data 
from helpers import db_to_geojson, search_db_time

# Configure application
app = Flask(__name__)

#now with heroku

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
  	

@app.route("/custom", methods=['POST', 'GET'])
def custom_map():
	if request.method == 'POST':
		starttime = request.form.get("starttime")
		endtime = request.form.get("endtime")
		color1 = request.form.get("color1")
		color2 = request.form.get("color2")
		
		if starttime == None:
			return render_custom()
		if starttime == '24':
			starttime = '0'
		if endtime == None:
			endtime = starttime

		datapoints = search_db_time(int(starttime), int(endtime))
		geojson = db_to_geojson(datapoints)
		
		night = is_night(int(starttime), int(endtime))
		style = night*'dark'

		return render_template("blank.html", title="custom map", geojson=geojson, night=night, style=style, color1=color1, color2=color2)
		
		# return render_template("blank.html", content =f"start: {starttime}\nend: {endtime}", title="TODO")
	return render_custom()


def is_night(starttime, endtime):
	if endtime < starttime:
		is_night = True
	else:
		if endtime >= 21 or starttime < 6:
			is_night = True
		else:
			is_night = False
	return is_night

def render_custom():
	time = list(range(0, 25))
	return render_template("custom.html", title="custom map", content="Select a time to plot on map", time=time)
  	
# TODO
@app.route("/mapday")
def mapday():
	datapoints = search_db_time(6, 21)
	geojson = db_to_geojson(datapoints)

	return render_template("blank.html", title="map at day", geojson=geojson)
  	

@app.route("/mapnight")
def mapnight():
	datapoints = search_db_time(22, 5)
	geojson = db_to_geojson(datapoints)
	return render_template("blank.html", title="map at night", geojson=geojson, style='dark', night=True)


@app.route("/general")
def general():
	sql = db.execute("SELECT * FROM location")

	points = []
	# [[long, lat, sensor, timestamp, user],]
	for i in range(len(sql)):
		points.append([sql[i]["long"], sql[i]["lat"], sql[i]["sensor"], sql[i]["timestamp"], sql[i]["user"]])

	features = geojson_pointfeature(points)

	featurecollection_general = geojson_featurecollection(features)

	return render_template("blank.html", title="general", geojson=featurecollection_general, style='dark', night=True)

  	
@app.route("/admin")
def admin():
  	return render_template("admin.html", title="admin")


@app.route("/mappoints", methods=['GET'])
def map_points():
	npoints = int(request.args.get('n'))
	geojson = geojson_rdm_points(npoints)
	return render_template("blank.html", title="mappoints", geojson=geojson)


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
		return render_template("blank.html", title="input app location", geojson=jsonlocation)
	else:
		return render_template("inputapplocation.html")

	
@app.route("/lastmap", methods=['GET'])
def map_last_map():
	global featurecollection
	return render_template("blank.html", title="lastmap", geojson=featurecollection)


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

	# converts a json from app to a geojson
	points = read_myjson(json_request)
	# save in Database SQL
	print(store_data(points))

	# transform on a json
	features = geojson_pointfeature(points)
	global featurecollection
	featurecollection = geojson_featurecollection(features)

	return 200, json_request


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


def apology(msg, code=400):
	msg_site = msg + "<br>code: " + str(code)
	return render_template("apology.html", title=f"error: {code}", content=msg_site)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)



# trying without app.run to heroku
# app.run(host='0.0.0.0', port=5000, debug=False) # Run the Application

