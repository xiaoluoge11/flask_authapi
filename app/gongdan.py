from flask_restful import Resource,reqparse
from app import api,auth,celery,mail
from flask import jsonify,g,request
from app.models import *
from utils import *
import json
from tasks import *

class GongdanAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        pagination = Gongdan.query.filter_by(userid=g.user.id).paginate(1,per_page=10,error_out=False)
        db.session.close()
        ret = pagination.items
        result = process_result(ret, [])
        for i in result:
            data_name=User.query.filter_by(id=int(i['applicant'])).first()
            i['shenqingman'] = data_name.username
        data = {'gongdan':result}
        data['total']=pagination.total
        return jsonify(data)
 
   
    def post(self):
        data = request.get_json()['params']
        data['applicant'] = g.user.id
        rows = [data]
        db.session.execute(Gongdan.__table__.insert(),rows)
        db.session.commit()
        data_name=User.query.filter_by(id=int(data['userid'])).first()
        data['to'] = data_name.email
        task=send_async_email.delay(data)
        return jsonify({'code':0,'msg':'添加成功','taskid':task.id}) 	


class EditGongdan(Resource):
    decorators = [auth.login_required]
    def put(self,id):
        db.session.query(Gongdan).filter_by(id=id).update({'status':1})
        ret = db.session.query(Gongdan).filter_by(id=id).all()
        data = process_result(ret, [])[0]
        data_name=User.query.filter_by(id=int(data['applicant'])).first()
        data['to'] = data_name.email
        data['comment']= "%s::工单处理中" %(data['comment'])
        task=send_async_email.delay(data)
        db.session.commit()  
        return jsonify({'code':0,'msg':'添加完成','taskid':task.id})


class FinshGongdan(Resource):
    decorators = [auth.login_required]
    def put(self,id):
        ret = db.session.query(Gongdan).filter_by(id=id).update({'status':2})
        ret = db.session.query(Gongdan).filter_by(id=id).all()
        data = process_result(ret, [])[0]
        data_name=User.query.filter_by(id=int(data['applicant'])).first()
        data['to'] = data_name.email
        data['comment']= "工单:%s::您的工单已经处理完成" %(data['comment'])
        task=send_async_email.delay(data) 
        db.session.commit()  
        return jsonify({'code':0,'msg':'工单关闭','taskid':task.id})


class BohuiGongdan(Resource):
    decorators = [auth.login_required]
    def post(self):
        data = request.get_json()['params']
        data['status'] = 3
        data.pop('shenqingman')
        data.pop('create_time')
        if not data['explain']:
            return jsonify({'code':10002,'msg':'请添加驳回说明'}) 
        ret = db.session.query(Gongdan).filter_by(id=data['id']).update(data)
        db.session.commit()
        data_name=User.query.filter_by(id=int(data['applicant'])).first()
        data['to'] = data_name.email
        data['comment']= "你的工单%s 已驳回,驳回理由是:%s" %(data['comment'],data['explain'])
        task=send_async_email.delay(data)
        db.session.commit()  
        return jsonify({'code':0,'msg':'工单驳回','taskid':task.id})




api.add_resource(GongdanAPI, '/devops/api/v1.0/gongdan', endpoint ='gongdan')
api.add_resource(EditGongdan, '/devops/api/v1.0/gongdan/<int:id>', endpoint ='gongdanedit')
api.add_resource(FinshGongdan, '/devops/api/v1.0/finsh/<int:id>',endpoint='finshgongdan')
api.add_resource(BohuiGongdan, '/devops/api/v1.0/bohuigongdan', endpoint
                 ='bohuigongdan') 
