#!/usr/bin/env python
#
# runserver.py : run server
#
from voiceauth.routes import app
from flask_cors import CORS, cross_origin
import os

CORS(app, resources=r'/*', allow_headers='*',origins='*', expose_headers='Authorization')
CORS(app, resources='/voiceauth', allow_headers='*',origins='*', expose_headers='Authorization')

DEBUG = int(os.environ["DEBUG"]) or 1
port = int(os.environ.get('PORT',5000))
host = '127.0.0.1' if DEBUG else '0.0.0.0'

if __name__ == "__main__":
    app.run(host=host,port=port,debug = DEBUG)
    print ("Voice Auth server started on port " + port)
