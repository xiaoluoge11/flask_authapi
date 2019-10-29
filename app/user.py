from flask_restful import Resource
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json

class UserAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        name = request.args.get('name')
        page = request.args.get('page',type=int)
        if not name:
            pagination = User.query.order_by(User.id.desc()).paginate(page,per_page=10,error_out=False)
            db.session.close()
            ret = pagination.items
            result = process_result(ret, [])
            data = {'users':result}  
            data['total']=pagination.total	
            return jsonify(data)
        else:
            pagination = User.query.filter(User.name.like('%' + name + '%')).paginate(page, per_page=10, error_out=False)
            ret = pagination.items	
            result = process_result(ret, [])
            data = {'users':result}
            data['total']=pagination.total
            return jsonify(data) 

api.add_resource(UserAPI, '/devops/api/v1.0/user', endpoint = 'user')
