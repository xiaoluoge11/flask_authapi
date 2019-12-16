# -*- coding: utf-8 -*-

import sys
import os
import utils

work_dir = os.path.dirname(os.path.realpath(__file__))
service_conf = os.path.join(work_dir, 'conf/service.conf')
config = utils.get_config(service_conf)

#{'mysql_host': '127.0.0.1', 'mysql_port': '3306', 'mysql_user': 'root', 'mysql_passwd': '123456', 'mysql_db': 'rest', 'mysql_charset': 'utf8'}

SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@{}:{}/{}?charset={}".format(config['mysql_user'], config['mysql_passwd'],config['mysql_host'],config['mysql_port'],config['mysql_db'],config['mysql_charset']) 
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLAlCHEMY_ECHO=True

# 安全配置
CSRF_ENABLED = True
SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'

#mail配置
# Flask-Mail configuration
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 25
MAIL_USE_TLS = True
MAIL_USERNAME = '942729042@qq.com'
MAIL_PASSWORD = 'tygowyeqpjprbebd'
MAIL_DEFAULT_SENDER = '942729042@qq.com'

# Celery configuration
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

#celery 时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'



if __name__=="__main__":
    print(config)
