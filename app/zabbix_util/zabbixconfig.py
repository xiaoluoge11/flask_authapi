from flask_restful import Resource,reqparse
from app import api,auth
from flask import jsonify,g,request
from app.models import *
from utils import *
import json
from zabbix_tree import *
from zabbix import *

class zabbixconfig():
    def __init__(self):
        ret = ZabbixConfig.query.all()
        result = process_result(ret, [])[0]
        self.zabbix = Zabbix(result['url'],result['username'],result['password'])
        self.jsondata = result
    def init_zb_host(self):
        data = self.zabbix.host_list()
        print(data)
        for host in data:
            host['groups'] = host['groups'][0]['name']
            hostid = Zabbix_host.query.filter_by(hostid=host['hostid']).all()
            if hostid:	
                db.session.query(Zabbix_host).filter_by(hostid=host['hostid']).update(host)
            else:
                db.session.execute(Zabbix_host.__table__.insert(),[host]) 
                db.session.commit() 
        return data
    def connet(self): 
        return self.jsondata

class ZabbixConfigAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        ret = ZabbixConfig.query.all()
        result = process_result(ret, [])
        data = {'zabbix':result}
        return jsonify(data)

    def post(self):
        data = request.get_json()['params']
        if not data['url']:
            return jsonify({'code':10003,'msg':'添加url'})
        try:
            Zabbix(data['url'],data['username'],data['password'])
            rows = [data]
            db.session.execute(ZabbixConfig.__table__.insert(),rows)
            db.session.commit()
            return jsonify({'code':0,'msg':'添加成功'})
        except:
            return jsonify({'code':10003,'msg':'添加失败'})



class ZabbixConfigUpdateAPI(Resource):
    decorators = [auth.login_required]
    def delete(self,id):
        obj = ZabbixConfig.query.filter_by(id=int(id)).first()
        db.session.delete(obj)
        db.session.commit()
        return  jsonify({'code':0,'msg':'删除成功'})

    def put(self,id):
        data = request.get_json()['params']
        data.pop('service')
        ret = db.session.query(Product).filter_by(id=id).update(data)
        db.session.commit()
        return json.dumps({'errcode':0})


class ZabbixConfigTreeAPI(Resource):        
    decorators = [auth.login_required]                                           
    def get(self):                      
        ret = ZabbixConfig.query.all()
        result = process_result(ret, [])[0]
        data = get_zabbix_treeview(result['url'],result['username'],result['password'])
        return jsonify(data)
 

class syncAPI(Resource):            
    decorators = [auth.login_required]                                               
    def get(self):                          
        zabbix_init = zabbixconfig()
        zabbix_init.init_zb_host() 
        data = Zabbix_host.query.all()
        result = process_result(data, ['host'])
        hosts = [i['host'] for i in result]
        ret = db.session.query(Server).filter(Server.ip.notin_(hosts)).all()
        result = process_result(ret, ['ip'])
        data = [i['ip'] for i in result]	
        return jsonify(data)

    def post(self):
        data = request.get_json()['params']
        data_result = []
        result = zabbixconfig().connet()
        zabbix_init=Zabbix(result['url'],result['username'],result['password'])
        #data = {u'hosts': [u'192.168.1.37', u'192.168.1.41'], u'value': u'10001'}
        for ip in data['hosts']:
            ret = zabbix_init.sync_host_zabbix(data['value'],ip, ip) 
            data_result.append(ret)
        return jsonify({'code':0,'msg':'添加成功'})



class GroupAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        result = zabbixconfig().connet()
        zabbix_init=Zabbix(result['url'],result['username'],result['password'])
        data=zabbix_init.group_list()
        return jsonify(data)


class TemplateAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        result = zabbixconfig().connet()                                    
        zabbix_init=Zabbix(result['url'],result['username'],result['password'])
        data = zabbix_init.template_list()
        return jsonify(data) 

    def post(self):
        ret = []
        data = request.get_json()['params']
        HostList = request.get_json()['ids']
        for i in HostList.split(','):
            hostip=Server.query.filter_by(id=int(i)).first()
            ret.append(hostip.ip)
        result = zabbixconfig().connet()                                                                    
        zabbix_init=Zabbix(result['url'],result['username'],result['password'])   	
        hostlist = zabbix_init.host_list()
        #{u'HostList': [u'192.168.1.35', u'192.168.1.37'], u'value': [u'10001', u'10047']}
        for host in ret:
            for hoststatus in list(filter(lambda x:True if x.get('host', None) == host else False, hostlist)):
                zabbix_init.link_template(hoststatus['hostid'],data['value'])	
        return jsonify({'code':0,'msg':'添加成功'})


class Product_ipAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        result = zabbixconfig().connet()
        zabbix_init=Zabbix(result['url'],result['username'],result['password'])
        id = request.args.get('id') 
        label = request.args.get('label') 
        id_data = Product.query.filter_by(id=int(id)).first()
        if int(id_data.pid) == 0:
            data = Server.query.filter_by(Product_id=int(id)).all()
            result = process_result(data, []) 
            for i in result: 
                host_data = list(filter(lambda x:True if x.get('host', None) ==
                                        i['ip'] else False,
                                        zabbix_init.host_list()))

                ret = zabbix_init.get_template(host_data[0]['hostid'])
                if ret:
                    ret = ','.join([item['name'] for item in ret])
                else:
                    ret = ''
                i['template'] = ret	
        else:
            data = Server.query.filter_by(Service_id=int(id)).all()
            result = process_result(data, [])
            for i in result:
                host = list(filter(lambda x:True if x.get('host', None) ==
                                   i['ip'] else False,
                                   zabbix_init.host_list()))
                ret = zabbix_init.get_template(host[0]['hostid'])
                if ret:
                    ret = ','.join([item['name'] for item in ret])
                else:
                    ret = ''
                i['template'] = ret
        return jsonify(result)
 

class zabbixlistAPI(Resource):
    decorators = [auth.login_required]
    def get(self):
        data = Zabbix_host.query.all()                                                                                        
        result = process_result(data, [])        
        return jsonify(result) 



api.add_resource(ZabbixConfigAPI, '/devops/api/v1.0/zabbixconfig', endpoint = 'zabbixconfig')
api.add_resource(ZabbixConfigUpdateAPI, '/devops/api/v1.0/zabbixconfig/<int:id>', endpoint = 'zabbixconf')
api.add_resource(ZabbixConfigTreeAPI, '/devops/api/v1.0/getZabbixTree', endpoint = 'zabbixconfigTree')
api.add_resource(syncAPI, '/devops/api/v1.0/Sync',endpoint ='sync')
api.add_resource(GroupAPI, '/devops/api/v1.0/getgroup',endpoint ='group')
api.add_resource(TemplateAPI, '/devops/api/v1.0/template',endpoint ='template')
api.add_resource(Product_ipAPI, '/devops/api/v1.0/getProduct_Ip',endpoint ='getProduct')
api.add_resource(zabbixlistAPI, '/devops/api/v1.0/zabbixlist',endpoint ='zabbixlist')
