import os
from flask import Flask, request, jsonify, render_template, make_response
import requests
import urllib.parse
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


app = Flask(__name__)


@app.route("/")
def index():
  	return '''
		Its working!<br><br>
		
		<a href="/location">/location<a><br>
		<a href="/postjson">/postjson<a><br>
		'''


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


@app.route('/postjson', methods=['POST', 'GET'])
def postjson():
	if request.method == "POST":
		a = request.get_json()
		
		if isinstance(a, dict):
			res = make_response(jsonify(a), 200)
			print("__response OK")
			
		else:
			formato = f"must be JSON, its a {type(a)}"
			res = make_response(jsonify({"message": formato}), 405)
			print(f"__Response error: {formato}")


		print(type(res.get_json()))
		
		return res 

	return '''Try to post a JSON<br>
					Example in <a href=https://colab.research.google.com/drive/1H-cBSzQcHqKl-CObhL1_tl76_76lynNX?usp=sharing>Colab<a>.'''


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

def apology(msg, code=400):
	return "<b>ERROR!</b> <br>name: " +msg + "<br>code: " + str(code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


app.run(host='0.0.0.0', port=5000, debug=False) # Run the Application (in debug mode)
