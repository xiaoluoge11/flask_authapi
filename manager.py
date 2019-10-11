#-*- coding:utf-8 -*-
#filename: manage.py

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import db,app
from app.models import *


migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
