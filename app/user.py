from flask_restful import Resource
from app import api,auth
from flask import jsonify,g
from app.models import *
from utils import *


class UserAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        users = User.query.all()
        result=process_result(users,[])
        return jsonify(result)

api.add_resource(UserAPI, '/devops/api/v1.0/user', endpoint = 'user')
