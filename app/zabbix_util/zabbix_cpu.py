from flask_restful import Resource,reqparse
import json,time
from pyzabbix import ZabbixAPI 
from flask import jsonify,g,request
from app import api,auth
zabbix = ZabbixAPI('http://192.168.75.133/zabbix')
zabbix.session.verify = False
zabbix.login('Admin', 'zabbix')  
hostid = '10306'


class CpuAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        res = zabbix.item.get(
        hostids=[hostid],
        output=["name",
            "key_",
            "value_type",
            "hostid",
            "status",
            "state"],
           filter={'key_': 'system.cpu.load[all,avg15]'})
        dump = json.dumps(res)
        itemid = res[0]['itemid']
        t_till = int(time.time())
        t_from = t_till - 2 * 24 * 60 * 60
        # 查询cpu历史数据
        history = zabbix.history.get(
            # hostids=[hostid],
            itemids=[itemid],
            history=0,
            output='extend',
            sortfield='clock',
            sortorder='ASC',
            time_from=t_from,
            time_till=t_till)
        json_dump = jsonify(history)
        print(json_dump)
        return json_dump

#vm.memory.size[available]


class MemoryAPI(Resource):
    decorators = [auth.login_required]

    def get(self):
        res = zabbix.item.get(
        hostids=[hostid],
        output=["name",
            "key_",
            "value_type",
            "hostid",
            "status",
            "state"],
           filter={'key_': 'vm.memory.size[pavailable]'})
        dump = json.dumps(res)
        itemid = res[0]['itemid']
        t_till = int(time.time())
        t_from = t_till - 2 * 24 * 60 * 60
        # 查询cpu历史数据
        history = zabbix.history.get(
            # hostids=[hostid],
            itemids=[itemid],
            history=0,
            output='extend',
            sortfield='clock',
            sortorder='ASC',
            time_from=t_from,
            time_till=t_till)
        json_dump = jsonify(history)
        print(json_dump)
        return json_dump

#vm.memory.size[available]









api.add_resource(CpuAPI, '/devops/api/v1.0/cpu', endpoint = 'cpu')
api.add_resource(MemoryAPI, '/devops/api/v1.0/memory', endpoint = 'memory')
