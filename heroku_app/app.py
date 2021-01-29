# app.py
from flask import Flask, request, jsonify
from parse_formula import parse_formula

app = Flask(__name__)


@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("formula", None)

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "Please enter a formula."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "Formula can't be fully numeric."
    # Now the user entered a valid name
    else:
        try:
            response["MESSAGE"] = parse_formula(str(name))
        except ValueError as e:
            response["ERROR"] = str(e)

    # Return the response in json format
    return jsonify(response)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, debug=True, port=5000)
