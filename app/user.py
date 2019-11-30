from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json

class UserListAPI(Resource):
    decorators = [auth.login_required]
 
    def get(self):
        name = request.args.get('name')
        page = request.args.get('page',type=int)
        user_role = []
        if not name:
            pagination = User.query.order_by(User.id.desc()).paginate(page,per_page=10,error_out=False)
            db.session.close()
            ret = pagination.items
            result = process_result(ret, []) 
            for i in result:
                user = User.query.filter_by(id=i['id']).first()	
                for k in user.roles:
                    if not k.name:
                        test = [user.id,{user.id:k.name}]
                    test = [user.id,{user.id:k.name}]
                    user_role.append(test)
                str_data = stru_key_value(user_role)  
            for ret in result:
                for key,value in str_data.items(): 
                    if ret['id'] == key:
                        ret['user_role'] = '::'.join(stru_data(value)) 
            data = {'users':result}  
            data['total']=pagination.total
            print(data)
            return jsonify(data)
        else:
            pagination = User.query.filter(User.name.like('%' + name + '%')).paginate(page, per_page=10, error_out=False)
            db.session.close()
            ret = pagination.items	
            result = process_result(ret, [])
            for i in result:
                user = User.query.filter_by(id=i['id']).first()
                for k in user.roles:
                    if not k.name:
                        test = [user.id,{user.id:k.name}]
                    test = [user.id,{user.id:k.name}]
                    user_role.append(test)
                str_data = stru_key_value(user_role)
            for ret in result:
                for key,value in str_data.items():
                    if ret['id'] == key:
                        ret['user_role'] = '-'.join(stru_data(value))
            data = {'users':result}
            data['total']=pagination.total
            return jsonify(data) 
    def post(self):
        data = request.get_json()['params']
        rows = [data]
        db.session.execute(User.__table__.insert(),rows)
        db.session.commit()
        return json.dumps({'errcode':0}) 


class UserAPI(Resource):
    decorators = [auth.login_required]
    def delete(self,id):
        obj = User.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()
        return  json.dumps({'errcode':0})       
    def put(self,id):
        data = request.get_json()['params']
        data.pop('id')
        if 'user_role' in data:
            data.pop('user_role')
        ret = db.session.query(User).filter_by(id=id).update(data)
        db.session.commit()              
        return json.dumps({'errcode':0}) 

class EditRoleUser(Resource):
    decorators = [auth.login_required]
    def put(self,id):
        data = request.get_json()['params']
        Role_data = []
        user = User.query.filter_by(id=int(id)).first()
        for i in data:
            Role_data.append(Role.query.filter_by(id=int(i)).first())
            user.roles=Role_data	
        db.session.commit()
        return json.dumps({'errcode':0})
 



api.add_resource(UserListAPI, '/devops/api/v1.0/user', endpoint = 'user')
api.add_resource(UserAPI, '/devops/api/v1.0/user/<int:id>', endpoint = 'useredit')
api.add_resource(EditRoleUser, '/devops/api/v1.0/editRoleUser/<int:id>', endpoint ='editRoleUser')
