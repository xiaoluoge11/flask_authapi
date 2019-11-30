# coding:utf-8
import datetime, time
import requests,time,json
from zabbix import *


"""
     1 server
	2 service
	    3 product
"""

#[{'groupid': '5', 'name': 'Discovered hosts'}, {'groupid': '7', 'name': 'Hypervisors'}, {'groupid': '2', 'name': 'Linux servers'}, {'groupid': '1', 'name': 'Templates'}, {'groupid': '12', 'name': 'Templates/Applications'}, {'groupid': '13', 'name': 'Templates/Databases'}, {'groupid': '8', 'name': 'Templates/Modules'}, {'groupid': '9', 'name': 'Templates/Network Devices'}, {'groupid': '10', 'name': 'Templates/Operating Systems'}, {'groupid': '11', 'name': 'Templates/Servers Hardware'}, {'groupid': '14', 'name': 'Templates/Virtualization'}, {'groupid': '6', 'name': 'Virtual machines'}, {'groupid': '4', 'name': 'Zabbix servers'}]


#[{'hostid': '10264', 'host': '192.168.100.37', 'name': '192.168.100.37', 'available': '0', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10270', 'host': '192.168.100.102', 'name': '192.168.100.102', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10271', 'host': '192.168.100.103', 'name': '192.168.100.103', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10272', 'host': '192.168.100.43', 'name': '192.168.100.43', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10273', 'host': '192.168.100.44', 'name': '192.168.100.44', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10274', 'host': '192.168.100.35', 'name': '192.168.100.35', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10275', 'host': '192.168.100.245', 'name': '192.168.100.245', 'available': '0', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10276', 'host': '192.168.100.101', 'name': '192.168.100.101', 'available': '2', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}, {'hostid': '10277', 'host': '10.3.0.43', 'name': '10.3.0.43', 'available': '1', 'groups': [{'groupid': '2', 'name': 'Linux servers'}]}]

#for i in data.group_list():
#        print(data.host_list(i['groupid']))



class Treeview():
    def __init__(self,url,username,password):
        self.url = url
        self.zabbix =Zabbix(url,username,password)

    def get_url(self):
        ret = []
        node={}
        node['label'] = self.url  
        node['children'] = self.get_child_node()       
        ret.append(node)
        return ret
    def get_child_node(self):
        ret = []
        for group in self.zabbix.group_list():
            node = {}
            node['label'] = group['name']
            node['children'] = self.get_grant_node(group['groupid'])
            ret.append(node)
        return ret

    def get_grant_node(self, id):
        ret = []
        for host in self.zabbix.host_list(id):
            node = {}
            node['label'] = host['host']
            ret.append(node)
        return ret

    def get(self):
        return self.get_url()

def get_zabbix_treeview(url,username,password):
    return Treeview(url,username,password).get()

if __name__ == "__main__":
    data=get_zabbix_treeview('http://192.168.75.133/zabbix','Admin','zabbix')
    print(data)
