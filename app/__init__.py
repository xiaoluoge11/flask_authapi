# -*- coding:utf-8 -*-

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_restful import Resource, Api

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
db = SQLAlchemy(app)
api=Api(app)
auth = HTTPBasicAuth()

from . import models, views, user
