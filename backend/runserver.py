#!/usr/bin/env python
#
# runserver.py : run server
#
from flask_cors import CORS, cross_origin
import os
from flask import Flask, make_response, request, current_app
from flask import jsonify, Response
from flask_restful import Resource, Api
import json
from flask_cors import CORS, cross_origin
import http.client, urllib.request, urllib.parse, urllib.error, base64
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


app = Flask(__name__)
api = Api(app)

msApiKey = "fbe9b16688bf4ba98e8d5d3631f10472"

cred = credentials.Certificate("./voiceauth/voiceauthkey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://voiceauth-88046.firebaseio.com/'
})

ref = db.reference('/users')
# print ref.get()


@app.errorhandler(400)
def bad_request(error=None):
    message = {
               'status': 400,
               'message': "Bad request."
               }
    resp = jsonify(message)
    resp.status_code = 400

    return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
                'status': 404,
                'message': 'Not Found: ' + request.url
              }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

@app.errorhandler(500)
def internal_error(error=None):
    message = {
                'status': 500,
                'message': 'Internal error! You can try again, or send a message to the administrator.'
              }
    resp = jsonify(message)
    resp.status_code = 500
    
    return resp
    
#Routing function

##Returns the UID for a username
@app.route('/voiceauth/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    if not request.json or not 'username' in request.json  or not 'password' in request.json  or not 'blob' in request.json:
        abort(400)

    username = request.json['username']
    password = request.json['password']
    blob = request.json['blob']


    url = "https://westus.api.cognitive.microsoft.com/spid/v1.0/identificationProfiles"
    headers = {
        'Content-Type': 'application/json',
        'ocp-apim-subscription-key': msApiKey
        }
    body = "{\'locale\':\'en-us\'}"

    response = requests.request("POST", url, headers=headers, data=body)
    data = response.json()
    msUID = data['identificationProfileId']

    ##voiceIt
    

    return jsonify({'identificationProfileId': data['identificationProfileId']}), 201



##Check if username exists, if not then create a uname in firebase and store pass
@app.route('/voiceauth/signup', methods=['POST', 'OPTIONS'])
@cross_origin()
def signup():
  if not request.json or not 'username' in request.json  or not 'password' in request.json:
        abort(400)

  username = request.json['username']
  password = request.json['password']

  snapshot = ref.child(username).get()

  if snapshot!=None:
    return jsonify({"result":"already exists"}), 201

  else:
    ref.child(username).push({
      'password':password
      })
    return jsonify({"result":"sucessful"}), 201


@app.route('/voiceauth/enroll', methods=['POST', 'OPTIONS'])
@cross_origin()
def enroll():
  if not request.json or not 'username' in request.json  or not 'blob' in request.json:
        abort(400)
  username = request.json['username']
  status = enroll_user(username,request.data)
  if status==1:
  	return jsonify({"result":"sucessful"}), 201





CORS(app, resources=r'/*', allow_headers='*',origins='*', expose_headers='Authorization')
CORS(app, resources='/voiceauth', allow_headers='*',origins='*', expose_headers='Authorization')

DEBUG = int(os.environ["DEBUG"]) or 1
port = int(os.environ.get('PORT',5000))
host = '127.0.0.1' if DEBUG else '0.0.0.0'

if __name__ == "__main__":
    app.run(host=host,port=port,debug = DEBUG)
    print ("Voice Auth server started on port " + port)
