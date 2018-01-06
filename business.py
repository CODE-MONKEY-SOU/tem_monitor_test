#-*- coding: UTF-8 -*-
import re
from model_ora import *
from flask_login import login_user
import config

datatype = {'1':'temperature','2':'intensity'}

def login_process(dic):
    user = BaseUser.query.filter_by(username=dic['username'],password=dic['password']).first()
    if user:
        login_user(user)
        return True
    else:
        return False

def upload_process(dic):
    print(dic)
    # if  not re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$",str(dic['ip'])):
    #     return "ip error"
    if not str(dic['datatype']) in datatype.keys():
        return "datatype error"
    de = DeviceMapping.objects(device_uid=dic['device_uid']).first()
    tem = TemperatureMapping(device_id=de.device_id,degree=float(dic['degree']))
    tem.save()

def query_device_process(dic):
    # datestart = datetime.datetime.strptime(dic['start'], '%Y-%m-%d')
    # dateend = datetime.datetime.strptime(dic['end'], '%Y-%m-%d')
    device_info = DeviceMapping.query.filter_by(device_macid=dic['macid']).first()
    device_info = device_info.toDict()
    return {'device_info':device_info}


def query_tem_process(dic):
    datestart = datetime.datetime.strptime(dic['start'], '%Y-%m-%d')
    datestart = datetime.datetime(datestart.year, datestart.month, datestart.day, 0, 0, 0)
    dateend = datetime.datetime.strptime(dic['end'], '%Y-%m-%d')
    dateend = datetime.datetime(dateend.year, dateend.month, dateend.day, 0, 0, 0)
    tem_info = TemperatureMapping.group_by_days(datestart, dateend, dic['macid'])
    return  tem_info

def query_tem_current_process(dic):
    # now  = datetime.datetime.now()
    # todaystart = datetime.datetime(now.year,now.month,now.day,0,0,0)-datetime.timedelta(days=1)
    # todayend = todaystart+datetime.timedelta(days=1)
    datestart = datetime.datetime.strptime(dic['start'], '%Y-%m-%d')
    dateend = datetime.datetime.strptime(dic['end'], '%Y-%m-%d')
    tlist=dict()
    if dateend - datestart <= datetime.timedelta(days=30):
        tlist = TemperatureMapping.date_range(datestart,dateend,dic['macid'])
    return tlist

def query_device_list_process():
    devices = DeviceMapping.query.filter_by(device_usingflag='1').all()
    arr = []
    for de in devices:
        arr.append(de.toDict())
    return arr
# def query_tem_lastest_process():
#     d_arr = TemperatureMapping.group_by_device_latest()
#     for dic in d_arr:
#         if dic['degree']>5:







