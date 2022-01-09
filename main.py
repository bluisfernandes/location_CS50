import os
from flask import Flask, request, jsonify, render_template, make_response
import requests
import urllib.parse
import json


app = Flask(__name__)

API_KEY = os.environ['API_KEY']

@app.route("/")
def index():
  	return "Its working!"

@app.route("/sum/<var1>,<var2>")
def sum(var1, var2):
	soma = int(var1) + int(var2)
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
		
		return res
		

	return render_template("location.html")

@app.route('/postjson', methods=['POST', 'GET'])
def postjson():
	if request.method == "POST":
		a = request.get_json()
		# a = request.get_data()
		res = make_response(jsonify(a), 200)
		print(res.get_json())

		return res

	return render_template("postjson.html")

print("iba")

app.run(host='0.0.0.0', port=5000, debug=True) # Run the Application (in debug mode)

# app.run(host='0.0.0.0')