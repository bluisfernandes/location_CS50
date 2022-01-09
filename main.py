import os
from flask import Flask, request, jsonify, render_template, make_response
import requests
import urllib.parse
import json
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError


app = Flask(__name__)

API_KEY = os.environ['API_KEY']


@app.route("/")
def index():
  	return '''
		Its working!<br><br>
		
		/sum/{var1},{var2}<br>
		/quote/{var1}<br>
		/location<br>
		/postjson<br>
		'''


@app.route("/sum/<var1>,<var2>")
def sum(var1, var2):
	soma = float(var1) + float(var2)
	print(soma)
	return str(soma)
	# return var


@app.route("/bye")
def bye():
	return "byebye"


@app.route("/quote/<var1>")
def quote(var1):
	return lookup(var1)


def lookup(symbol):
    """Look up quote for symbol."""

    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://cloud.iexapis.com/stable/stock/{urllib.parse.quote_plus(symbol)}/quote?token={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            # "name": quote["companyName"],
            # "price": float(quote["latestPrice"]),
            # "symbol": quote["symbol"]
			"z" : quote
        }
    except (KeyError, TypeError, ValueError):
        return None


@app.route('/location', methods=['POST', 'GET'])
def location():
	if request.method == "POST":
		a = request.form.get("username")
		b = json.loads(a)

		res = make_response(jsonify(b), 200)

		if isinstance(b, dict):
			res = make_response(jsonify(b), 200)
		
		else:
			res = make_response(jsonify({"message": "must be JSON"}), 405)
		
		return res
		
	return render_template("location.html")


@app.route('/postjson', methods=['POST', 'GET'])
def postjson():
	if request.method == "POST":
		a = request.get_json()
		# a = request.get_data()
		print(type(a))
		res = make_response(jsonify(a), 200)
		print(res.get_json())

		# return res
		if isinstance(a, dict):
			res = make_response(jsonify(a), 200)
		
		else:
			formato = f"must be JSON, its a {type(a)}"
			res = make_response(jsonify({"message": formato}), 405)
			print(formato)
		
		return res

	return '''Try to post a JSON<br>
					Example in <a href=https://colab.research.google.com/drive/1H-cBSzQcHqKl-CObhL1_tl76_76lynNX?usp=sharing>Colab<a>.'''


print("restart")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return "Error! <br>name: " +e.name + "<br>code: " + str(e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

app.run(host='0.0.0.0', port=5000, debug=True) # Run the Application (in debug mode)
