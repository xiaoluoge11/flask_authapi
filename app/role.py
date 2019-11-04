from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json

class RoleListAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        name = request.args.get('name')
        page = request.args.get('page',type=int)
        if not name:
            pagination = Role.query.order_by(Role.id.desc()).paginate(page,per_page=10,error_out=False)
            ret = pagination.items
            result = process_result(ret, [])
            data = {'roles':result}
            data['total']=pagination.total
            print(data)
            return jsonify(data)
        else:
            pagination = Role.query.filter(Role.name.like('%' + name + '%')).paginate(page, per_page=10, error_out=False)
            ret = pagination.items
            result = process_result(ret, [])
            data = {'roles':result}
            data['total']=pagination.total
            return jsonify(data)
   
    def post(self):
        data = request.get_json()['params']
        rows = [data]
        db.session.execute(Role.__table__.insert(),rows)
        db.session.commit()
        return json.dumps({'code':0,'msg':'添加成功'}) 		


class RoleAPI(Resource):
    decorators = [auth.login_required]
    def delete(self,id):
        obj = Role.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()
        return  json.dumps({'code':0,'msg':'成功'})
    def put(self,id):
        data = request.get_json()['params']
        data.pop('id')                    
        ret = db.session.query(Role).filter_by(id=id).update(data)
        db.session.commit()              
        return json.dumps({'code':0,'msg':'更新成功'}) 





api.add_resource(RoleListAPI, '/devops/api/v1.0/role', endpoint = 'role')
api.add_resource(RoleAPI, '/devops/api/v1.0/role/<int:id>', endpoint = 'roleedit')

