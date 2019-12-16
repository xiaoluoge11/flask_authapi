# coding=utf-8
import time
from pyzabbix import ZabbixAPI

# 登录zabbix

class Zabbix():
    def __init__(self,url,zabbix_name,password):
        self.zabbix = ZabbixAPI(url)	
        self.zabbix.login(zabbix_name,password)


    def group_list(self):
        return self.zabbix.hostgroup.get(output=['groupid', 'name'])


    def template_list(self):
        return self.zabbix.template.get(output=['name'])


    def host_list(self,group=None):
        if group:
            return self.zabbix.host.get(
                output=['host', 'hostid', 'name',
                        'available','maintenance_status','maintenanceid'],
                groupids=[group],
                selectGroups=['name']
            )
        else:
            return self.zabbix.host.get(output=['host', 'hostid', 'name',
                                                'available','maintenance_status','maintenanceid'],selectGroups=['name'])


    def cpu_list(self,hostid):
        if hostid:
            item = self.zabbix.item.get(hostids=[hostid], output=["name", "key_", "value_type", "hostid", "status", "state"],filter={'key_': 'system.cpu.load[percpu,avg1]'})
            itemid = item[0]['itemid']
            t_till = int(time.time())
            t_from = t_till - 2 * 24 * 60 * 60

            return self.zabbix.history.get( itemids=[itemid],history=0,output='extend',sortfield='clock',sortorder='ASC',time_from=t_from,time_till=t_till)


    def memory_list(self,hostid):
        if hostid:
            item = self.zabbix.item.get(hostids=[hostid], output=["name", "key_", "value_type", "hostid", "status", "state"],filter={'key_': 'vm.memory.size[available]'})
            itemid = item[0]['itemid']
            t_till = int(time.time())
            t_from = t_till - 2 * 24 * 60 * 60

            return self.zabbix.history.get( itemids=[itemid],history=3,output='extend',sortfield='clock',sortorder='ASC',time_from=t_from,time_till=t_till)


    def disk_list(self,hostid):
        if hostid:
            item = self.zabbix.item.get(hostids=[hostid], output=["name", "key_", "value_type", "hostid", "status", "state"],filter={'key_': 'vfs.fs.size[/,free]'})
            itemid = item[0]['itemid']
            t_till = int(time.time())
            t_from = t_till - 2 * 24 * 60 * 60

            return self.zabbix.history.get( itemids=[itemid],history=3,output='extend',sortfield='clock',sortorder='ASC',time_from=t_from,time_till=t_till)


    def event_list(self):
        t_till = int(time.time())
        t_from = t_till - 7 * 24 * 60 * 60
        triggers = self.zabbix.trigger.get(output=['triggerid', 'description', 'priority'])
        triggerDict = {}
        for trigger in triggers:
            triggerDict[trigger['triggerid']] = trigger
        events = self.zabbix.event.get(output='extend',selectHosts=['name', 'host'],sortfield='clock',sortorder='DESC',time_from=t_from,time_till=t_till,limit=100)
        return [{'clock': event['clock'],'eventid': event['eventid'],'acknowledged': event['acknowledged'],'hosts': event['hosts'],'trigger': triggerDict.get(event['objectid'])} for event in events]


    def usage(self,hostid):
        diskItemids = self.zabbix.item.get(hostids=[hostid],
               output=["name",
                "key_",
                "value_type",
                "hostid",
                "status",
                "state"],
              filter={'key_': 'vfs.fs.size[/,pfree]'}
              )
        diskUsage = self.zabbix.history.get(itemids=[diskItemids[0]['itemid']], history=0, output='extend', sortfield='clock',sortorder='ASC', limit=1)
        cpuItemids = self.zabbix.item.get(hostids=[hostid],
        output=["name",
                "key_",
                "value_type",
                "hostid",
                "status",
                "state"],
            filter={'key_': 'system.cpu.load[percpu,avg1]'}
          )
        cpuUsage = self.zabbix.history.get(itemids=[cpuItemids[0]['itemid']], history=0, output='extend', sortfield='clock',sortorder='ASC', limit=1)

        memoryItemids = self.zabbix.item.get(hostids=[hostid],
        output=["name",
                "key_",
                "value_type",
                "hostid",
                "status",
                "state"],
            filter={'key_': 'vm.memory.size[used]'}
        )
        memoryUsage = self.zabbix.history.get(itemids=[memoryItemids[0]['itemid']], history=0, output='extend',
                                     sortfield='clock',
                                     sortorder='ASC', limit=1)
        hosts = self.zabbix.host.get(output=['host', 'hostid', 'name', 'available'], hostids=[hostid], )

        return [{'host': hosts[0],'diskUsage': diskUsage,'cpuUsage': cpuUsage,'memoryUsage': memoryUsage,}]


    def service_history_list(self,service):
        if service:
            t_till = int(time.time())
            t_from = t_till - 7 * 24 * 60 * 60
            # 所有监控项
            items = self.zabbix.item.get(output=['itemid'],filter={'name': service},selectHosts=['name', 'host'],)
            history = []
            for item in items:
                history.append(self.zabbix.history.get(itemids=[item['itemid']],history=3,output='extend',sortfield='clock',sortorder='ASC',time_from=t_from,time_till=t_till,))
            return {'items': items,'history': history}


    def service_item_list(self,service):
        if service:
            # 所有监控项
            items = self.zabbix.item.get(output=['itemid'],filter={'name': service},selectHosts=['name', 'host'],)
            return items


    def history_list(self,itemid):
        if itemid:
            t_till = int(time.time())
            t_from = t_till - 7 * 24 * 60 * 60
            return self.zabbix.trend.get(itemids=[itemid],output='extend',time_from=t_from,time_till=t_till,)


    def all_usage(self):
        diskItemids = self.zabbix.item.get(output=["name","key_","value_type","hostid","status","state"],filter={'key_': 'vfs.fs.size[/,pfree]'})
        diskUsage = self.zabbix.history.get(itemids=[diskItemids[0]['itemid']], history=0, output='extend',sortfield='clock',sortorder='ASC', limit=1)
        return None


    def create_host(self,group_id, host_name, host_ip, template_id):
        host = self.zabbix.host.create(host=host_name,interfaces=[
               {
                'type': 1,
                'main': 1,
                'useip': 1,
                'ip': host_ip,
                'dns': '',
                'port': '10050'
              }
         ],
        groups=[{'groupid': group_id}],
        templates=[
        {
                'templateid': template_id,
             },
           ]
         )
        return host

    def sync_host_zabbix(self,group_id,host_name, host_ip):
        data = {
             "host": host_name,
               "interfaces": [
              {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": host_ip,
                "dns": "",
                "port": "10050"
               }
            ],
          "groups": [
             {
                "groupid": group_id
             }
           ]
          }    
        ret = self.zabbix.host.create(data)
        return ret

    def link_template(self,hostid, templateids):
        templates = []
        for id in templateids:
            templates.append({"templateid": id})
        try: 
            ret = self.zabbix.host.update(hostid=hostid, templates=templates)
            return ret
        except Exception as e:
            return e.message

    def get_template(self,hostid):
        return self.zabbix.template.get(hostids=hostid, output=["templateid","name"]) 

    def create_maintenance(self,name="test",hostids=10314,period=3600):
        data =  {
            "name": name,
            "active_since": int(time.time()),
            "active_till": int(time.time()) + period,
            "hostids": [
                hostids
            ],
            "timeperiods": [
                {
                    "timeperiod_type": 0,
                    "period": period
                }
            ]
        }
        ret = self.zabbix.maintenance.create(data)
        return ret
    ################获取维护周期，，#########################
    def get_maintenance(self):
        data = {
            "output": "extend",
            "selectGroups": "extend",
            "selectTimeperiods": "extend"
        }
        ret = self.zabbix.maintenance.get(data)
        return ret
    ##############获取维护周期之后，通过传入maintenanceid删除维护周期###########
    def del_maintenance(self,maintenanceids):
        return self.zabbix.maintenance.delete(maintenanceids) 


if __name__ == "__main__":
    data = Zabbix('http://192.168.75.133/zabbix','Admin','zabbix')
    print(data.event_list())
