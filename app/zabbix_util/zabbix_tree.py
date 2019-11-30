from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json
from tree import *

class TreeAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        ret = Product.query.all()
        result = process_result(ret, [])
        print(result)
        data = get_treeview(result) 
        return jsonify(data)











api.add_resource(TreeAPI, '/devops/api/v1.0/getTree', endpoint = 'tree')

