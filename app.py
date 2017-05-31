#!/usr/bin/env python

import urllib
import json
import os

from pprint import pprint
from flask import Flask
from flask import request
from flask import make_response
from flask import url_for
from flask import redirect

# Flask app should start in global layout
app = Flask(__name__, static_url_path="/static")

data_file =  open('drug.json')    
data = json.load(data_file)


@app.route('/bot')
def bot():
    app.send_static_file("bot.html")

@app.route('/', methods=['GET'])
def root():
	return "Sample webhook to connect to api.ai chatbot."

	
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    speech = "Specified medicine name is either invalid or not present in our database. Check again"
    action = req.get("result").get("action")
    result = req.get("result")
    parameters = result.get("parameters")


    if action == "pharma.description":
        # pharma description 
        speech = description(parameters)

    elif action == "pharma.dosage":
        # pharma dosage intent
        speech = dosage(parameters)

    elif action == "pharma.side_effects":
        # pharma side effects intent
        speech = side_effects(parameters)

    else:
        return {}

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


def description(parameters):
    med_received_title = parameters.get("any")

    speech = ""

    for med in data["drugs"]:
        if med["title"].lower() == med_received_title.lower():
            speech = med["title"] + "<br><br>" + med["description"] + "<br>" + med["dosage"] + "<br>" + med["side_effects"]
            speech = speech.encode('utf-8')

    print("Response:")
    print(speech)

    return speech

def dosage(parameters):
    med_received_title = parameters.get("any")

    speech = ""

    for med in data["drugs"]:
        if med["title"].lower() == med_received_title.lower():
            speech = med["title"] + "<br><br>" + med["dosage"]
            speech = speech.encode('utf-8')

    print("Response:")
    print(speech)

    return speech

def side_effects(parameters):
    med_received_title = parameters.get("any")

    speech = ""

    for med in data["drugs"]:
        if med["title"].lower() == med_received_title.lower():
            speech = med["title"] + "<br><br>" + med["side_effects"]
            speech = speech.encode('utf-8')

    print("Response:")
    print(speech)

    return speech


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
