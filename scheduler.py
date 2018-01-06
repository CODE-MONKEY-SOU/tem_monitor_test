#-*- coding: UTF-8 -*-
from model_ora import *
from config import *
from wechator import *


def temperature_warning_scheduler():
    d_arr = TemperatureMapping.group_by_device_latest()

    for dic in d_arr:
        if dic['degree']>WARNING_TEM_LINE:
            message = warning_meassage_tem_formater(dic)
            managers = BaseUser.query.filter_by(manager_flag='1')
            for user in managers:
                message_sender(user.wechat_nickname,message,user.wechat_remarkname)
    print('scheduler job query_tem_lastest_process finish')





