# coding:utf-8
import datetime, time
import requests,json
import time,MySQLdb

"""
	2 service
	    3 product
"""

class Treeview():
    def __init__(self,product):
        self.product_info = product
    
    def get_child_node(self):
        ret = []
        for product in filter(lambda x:True if x.get('pid', None) ==0 else False, self.product_info):
            node = {}
            node['label'] = product['service_name']
            node['id'] = product['id']
            node['children'] = self.get_grant_node(product['id'])
            ret.append(node)
        return ret

    def get_grant_node(self, id):
        ret = []
        for product in filter(lambda x:True if x.get('pid', None) ==id else False, self.product_info):
            node = {}
            node['label'] = product['service_name']
            node['id'] = product['id'] 
            ret.append(node)
        return ret

    def get(self):
        return self.get_child_node()

def get_treeview(data):
    return Treeview(data).get()

if __name__ == "__main__":
   data = [{'comment': None, 'dev_interface': '张飞', 'pid': 0, 'service_name': '直播', 'op_interface': '赵云', 'module_letter': 'on_line', 'id': 2}, {'comment': None, 'dev_interface': '马超', 'pid': 0, 'service_name': '录音', 'op_interface': '张飞', 'module_letter': 'vdios', 'id': 4}, {'comment': 'nginx 负载均衡', 'dev_interface': None, 'pid': 2, 'service_name': 'nginx', 'op_interface': None, 'module_letter': '', 'id': 6}, {'comment': '', 'dev_interface': None, 'pid': 2, 'service_name': 'mysql', 'op_interface': None, 'module_letter': '', 'id': 7}, {'comment': '录音web', 'dev_interface': None, 'pid': 4, 'service_name': 'nginx', 'op_interface': None, 'module_letter': '', 'id': 8}, {'comment': 'tomcat微服务', 'dev_interface': None, 'pid': 4, 'service_name': 'tomcat', 'op_interface': None, 'module_letter': '', 'id': 9}, {'comment': None, 'dev_interface': '赵云', 'pid': 0, 'service_name': '电商', 'op_interface': '刘备', 'module_letter': 'on_bus', 'id': 10}, {'comment': '电商', 'dev_interface': None, 'pid': 10, 'service_name': 'php', 'op_interface': None, 'module_letter': '', 'id': 11}]
   print(get_treeview(data))
 
