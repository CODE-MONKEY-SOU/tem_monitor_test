# -*- coding: UTF-8 -*-

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'
SQLALCHEMY_DATABASE_URI = 'oracle://tem_monitor:shy88808875@127.0.0.1:1521/orcl'
SQLALCHEMY_TRACK_MODIFICATIONS = True
DB_IP = '127.0.0.1'
DB_PORT = 27017
DB_NAME = 'tem_monitor'

# JOBS = [
#     {
#         'id': 'job1',
#         'func': 'scheduler:temperature_warning_scheduler',
#         'args': '',
#         'trigger': 'interval',
#         'seconds': 1
#     }
# ]
SCHEDULER_API_ENABLED = True
WARNING_TEM_LINE = 20

ITCHAT_CONTENT_FUNC_MAP = {'addUser': ['启动机器人', '启动自动回复'], 'removeUser': ['关闭机器人', '关闭自动回复'],
                           'switchEN': ['启动英语模式', '关闭中文模式', 'English Mode On', 'Chinese Mode Off'],
                           'switchZH': ['关闭英语模式', '启动中文模式', 'English Mode Off', 'Chinese Mode On']}


