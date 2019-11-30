from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json

class ServiceListAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        name = request.args.get('name')
        page = request.args.get('page',type=int) 
        data_filter = []
        if not name:
            pagination = Product.query.order_by(Product.id.desc()).paginate(page,per_page=10,error_out=False)
            db.session.close()
            ret = pagination.items
            result = process_result(ret, [])
            for product in filter(lambda x:True if x.get('pid', None) != 0 else False, result):
                product['service'] = (Product.query.filter_by(id=product['pid']).first()).service_name
                data_filter.append(product)
            data = {'product':data_filter}
            data['total']=pagination.total
            return jsonify(data)
        else:
            pagination = Product.query.filter(Product.service_name.like('%' + name + '%')).paginate(page, per_page=10, error_out=False)
            ret = pagination.items
            result = process_result(ret, [])
            for product in filter(lambda x:True if x.get('pid', None) != 0 else False, result):
                product['service'] = (Product.query.filter_by(id=product['pid']).first()).service_name
                data_filter.append(product)
            data = {'product':data_filter}
            data['total']=pagination.total
            return jsonify(data) 
   
    def post(self):
        data = request.get_json()['params']
        rows = [data] 
        db.session.execute(Product.__table__.insert(),rows)
        db.session.commit()
        return json.dumps({'code':0,'msg':'添加成功'}) 		


class ServiceAPI(Resource):
    decorators = [auth.login_required]
    def delete(self,id):
        obj = Product.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()
        return  json.dumps({'code':0,'msg':'成功'})

    def put(self,id):
        data = request.get_json()['params']
        data.pop('id')   
        data.pop('service')
        data.pop('service_name')
        ret = db.session.query(Product).filter_by(id=id).update(data)
        db.session.commit()              
        return jsonify({'code':0,'msg':'更新成功'}) 

class Product_pid(Resource):
    decorators = [auth.login_required]

    def get(self):
        data = []
        ret = Product.query.all()
        result = process_result(ret, [])
        for product in filter(lambda x:True if x.get('pid',None) == 0 else False, result):
            data.append(product)
        return jsonify(data)





api.add_resource(ServiceListAPI, '/devops/api/v1.0/service', endpoint ='service')
api.add_resource(ServiceAPI, '/devops/api/v1.0/service/<int:id>', endpoint ='serviceedit')
api.add_resource(Product_pid, '/devops/api/v1.0/get_pid_product', endpoint='product_pid')
