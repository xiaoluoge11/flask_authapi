from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json

class ServerListAPI(Resource):
    decorators = [auth.login_required]

    @role_required
    def get(self):
        name = request.args.get('name')
        page = request.args.get('page',type=int)
        user_role = []
        if not name:
            pagination = Server.query.order_by(Server.id.desc()).paginate(page,per_page=10,error_out=False)
            db.session.close()
            ret = pagination.items
            result = process_result(ret, []) 
            data = {'server':result}  
            data['total']=pagination.total
            print(data)
            return jsonify(data)
        else:
            pagination = Server.query.filter(Server.ip.like('%' + name + '%')).paginate(page, per_page=10, error_out=False)
            db.session.close()
            ret = pagination.items	
            result = process_result(ret, [])
            data = {'server':result}
            data['total']=pagination.total
            return jsonify(data) 
    def post(self):
        data = request.get_json()
        ret = Server.query.filter_by(mac_address=data['mac_address']).first()
        if ret:
            return jsonify({'code':100001,'msg':'该主机已经存在'})
        rows = [data]
        db.session.execute(Server.__table__.insert(),rows)
        db.session.commit()
        return jsonify({'code':0,'msg':'插入成功'}) 


class ServerAPI(Resource):
    decorators = [auth.login_required]
    def delete(self,id):
        obj = Server.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()
        return  jsonify({'code':0,'msg':'更新成功'})       
    def put(self,id):
        data = request.get_json()['params']
        data.pop('id') 
        ret = db.session.query(Server).filter_by(id=id).update(data)
        db.session.commit()              
        return jsonify({'code':0,'msg':'更新成功'})  




api.add_resource(ServerListAPI, '/devops/api/v1.0/server', endpoint ='server')
api.add_resource(ServerAPI, '/devops/api/v1.0/server/<int:id>', endpoint ='serveredit')
