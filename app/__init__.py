# -*- coding:utf-8 -*-

from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_cors import CORS
from flask_restful import Resource, Api
from flask_mail import Mail, Message
from celery import Celery

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config.from_object('config')
db = SQLAlchemy(app)
# Initialize extensions
mail = Mail(app)                                                                  
# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

api=Api(app)
auth = HTTPBasicAuth()

from . import models,views,user,role,server,product,service,gongdan
from .zabbix_util import zabbixconfig,zabbix_cpu,zabbix_tree
