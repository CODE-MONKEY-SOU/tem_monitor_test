# -*- coding: UTF-8 -*-
import datetime
from tem_monitor import db
from flask_login import UserMixin
from sqlalchemy import *
from sqlalchemy.orm import *
import random
import json
import config


# 定义User对象:
class BaseUser(db.Model, UserMixin):
    # 表的名字:
    __tablename__ = 'base_user'
    # 表的结构:
    id = db.Column(db.String(32))
    usid = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(20))
    password = db.Column(db.String(20))
    wechat_nickname = db.Column(db.String(200))
    wechat_remarkname = db.Column(db.String(200))
    manager_flag = db.Column(db.String(1))
    department = db.Column(db.String(255))
    position = db.Column(db.String(255))

    def __init__(self, username, password):
        self.username = username
        self.password = password


# 定义LocationDeviceMap
class LocationDeviceMap(db.Model):
    __tablename__ = 'location_device_map'
    location_id = db.Column(db.String(32), primary_key=True)
    device_id = db.Column(db.String(32), primary_key=True)

    def __init__(self, location_id, device_id):
        self.location_id = location_id
        self.device_id = device_id


DEVICETYPE_MAP = {1: '温控传感器', 2: '电流传感器'}



# 定义DeviceMapping
class DeviceMapping(db.Model):
    __tablename__ = 'device_mapping'
    device_macid = db.Column(db.String(32), primary_key=True)
    device_type = db.Column(db.Integer)
    device_name = db.Column(db.String(255))
    device_usingflag = db.Column(db.String(1))
    supervise_type = db.Column(db.INTEGER)
    supervise_name = db.Column(db.String(255))
    supervise_area = db.Column(db.INTEGER)
    supervise_floor = db.Column(db.INTEGER)
    supervise_highflag = db.Column(db.INTEGER)

    def __init__(self, device_macid, device_type, device_name, device_usingflag):
        self.device_macid = device_macid
        self.device_name = device_name
        self.device_type = device_type
        self.device_usingflag = device_usingflag

    def toDict(self):
        return {'device_name': self.device_name, 'device_type': self.device_type,
                'device_macid': self.device_macid ,'supervise_type':self.supervise_type,'supervise_name':self.supervise_name,'supervise_area':self.supervise_area,'supervise_highflag':self.device_usingflag}


class TemperatureMapping(db.Model):
    __tablename__ = 'temperature_mapping'
    device_id = db.Column(db.String(32), primary_key=True)
    degree = db.Column(db.Float)
    systime = db.Column(db.DateTime)

    def __init__(self, device_id, degree, systime):
        self.device_id = device_id
        self.degree = degree
        self.systime = systime

    @classmethod
    def group_by_days(cls, datestart, dateend, device_macid):
        print(datestart, dateend)
        rs = db.session.execute(
            'select to_char(t.systime,\'yyyy-mm-dd\') as days,avg(t.degree) as degree '
            'from temperature_mapping t,device_mapping d '
            'where t.device_id = d.device_id and to_char(t.systime,\'yyyy-mm-dd hh24:mi:ss\')>=\'%s\' and to_char(t.systime,\'yyyy-mm-dd hh24:mi:ss\')<\'%s\' and d.device_macid = \'%s\' '
            'group by to_char(t.systime,\'yyyy-mm-dd\')' % (datestart, dateend, device_macid))
        d = []
        for row in rs:
            d.append({'time': row[0], 'value': round(float(row[1]), 2)})
        return d

    @classmethod
    def group_by_months(cls, datestart, dateend, device_macid):
        rs = db.session.execute(
            'select to_char(t.systime,\'yyyy-mm\') as days,avg(t.degree) as degree '
            'from temperature_mapping t,device_mapping d '
            'where t.device_id = d.device_id and to_char(t.systime,\'yyyy-mm\')>=\'%s\' and to_char(t.systime,\'yyyy-mm\')<\'%s\' and d.device_macid = \'%s\' '
            'group by to_char(t.systime,\'yyyy-mm\')'
            'order by days' % (datestart, dateend, device_macid))
        d = []
        for row in rs:
            d.append({'time': row[0], 'value': round(float(row[1]), 2)})
        return d

    @classmethod
    def date_range(cls, datestart, dateend, device_macid):
        rs = db.session.execute(
            'select to_char(t.systime,\'yyyy-mm-dd hh24:mi:ss\') as days,t.degree as degree '
            'from temperature_mapping t,device_mapping d '
            'where t.device_id = d.device_id and to_char(t.systime,\'yyyy-mm-dd hh24:mi:ss\')>=\'%s\' '
            'and to_char(t.systime,\'yyyy-mm-dd hh24:mi:ss\')<\'%s\' and d.device_macid = \'%s\' order by days' % (
            datestart, dateend, device_macid))
        d = []
        for row in rs:
            d.append({'time': row[0], 'value': round(float(row[1]), 2)})
        return d

    @classmethod
    def group_by_device_latest(cls):
        rs = db.session.execute(
            'SELECT d.DEVICE_MACID,d.DEVICE_NAME,t.SYSTIME,t.DEGREE from ( '
            '  SELECT a.*,ROW_NUMBER() OVER(PARTITION BY a.DEVICE_ID ORDER BY a.SYSTIME DESC) RN '
            '  FROM  TEMPERATURE_MAPPING a) t '
            'LEFT JOIN DEVICE_MAPPING d '
            'ON t.DEVICE_ID=d.DEVICE_ID '
            'where t.RN=1')
        d = []
        for row in rs:
            d.append({'macid': row[0], 'name': row[1], 'time': row[2], 'degree': round(float(row[3]), 2)})
        return d

class ElectricityMapping(db.Model):
    __tablename__ = 'electricity_mapping'
    device_id = db.Column(db.String(32), primary_key=True)
    intensity = db.Column(db.Float)
    systime = db.Column(db.DateTime)

    def __init__(self, device_id, intensity, systime):
        self.device_id = device_id
        self.intensity = intensity
        self.systime = systime

