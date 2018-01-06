#-*- coding: UTF-8 -*-
from mongoengine import *
from datetime import *
from flask_login import UserMixin
from random import *
import pymongo
import config

class TemperatureMapping(Document):
    device_id = StringField(required=True)
    degree = FloatField(required=True)
    systime = DateTimeField(required=True,default=datetime.now())

    @classmethod
    def group_by_systime(cls,datestart,dateend,device_id):
        db = pymongo.MongoClient(host=config.DB_IP,port=config.DB_PORT).tem_monitor
        collection = db.temperature_mapping
        cursor = collection.aggregate(
            [
                # {"$match": {"device_id": device_id,"systime":{{"$gte":datestart},{"$lt":dateend}}}},
                # {"$match": {"device_id": device_id}},
                {"$group": {"systime":{"$dateToString":{ format: "%Y-%m-%d", date: "$systime" }}, "count": {"$sum": 1}}}
            ]
        )
        for i in cursor:
            print(i)

class LocationMapping(Document):
    location_id=StringField(max_length=20,required=True)
    location_name=StringField(required=True)
    location_ip=StringField(required=True)


class DeviceMapping(Document):
    device_id=StringField(max_length=32,required=True)
    device_uid=StringField(required=True)
    device_type=IntField(required=True)
    device_name=StringField(required=True)

class LocationDeviceMap(Document):
    location_id = StringField(required=True)
    device_id = StringField(required=True)

class User(UserMixin,Document):
    uid = StringField(required=True)
    username = StringField(required=True)
    password = StringField(required=True)

if __name__ == '__main__':
    TemperatureMapping.group_by_systime(datestart=datetime.strptime('2017-01-01','%Y-%m-%d'),dateend=datetime.now(),device_id='000001')
    # connect('tem_monitor')
    # end = datetime.now()
    # start = datetime.strptime('2017-01-01','%Y-%m-%d')
    # d4json = dict()
    # print(datetime.now())
    # while start < end:
    #     TemperatureMapping.
    #     start += timedelta(days=1)
    # # while start<end:
    # #     d4json.update({datetime.strftime(start,'%Y-%m-%d'):round(TemperatureMapping.objects(systime__gte=start,systime__lt=start+timedelta(days=1)).average('degree'),2)})
    # #     start += timedelta(days=1)
    # print(d4json)
    # print(datetime.now())


