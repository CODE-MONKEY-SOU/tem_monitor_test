#-*- coding: UTF-8 -*-
import itchat
from itchat.content import *
from config import *


class ContentFilter:
    def contentFilter(self, content, friend):
        '''
        invoke the function whose keyword is in content by reflection
        :param content:
        :param friend:
        :return:
        '''
        for funcname in ITCHAT_CONTENT_FUNC_MAP.keys():
            for keyword in ITCHAT_CONTENT_FUNC_MAP[funcname]:
                if content == keyword.encode('utf-8'):
                    getattr(self,funcname)(friend)
                    return True
        return False




@itchat.msg_register(TEXT, isGroupChat=False)
def message_receiver(msg):
    fromuser = itchat.search_friends(userName=msg['FromUserName'])

def message_sender(nickname,content,remarkname=''):
    if not nickname=='' or nickname==None:
        if remarkname == '' or remarkname == None:
            friend = itchat.search_friends(nickName=nickname)[0]
            itchat.send_msg(content, toUserName=friend['UserName'])
        else:
            friend = itchat.search_friends(nickName=nickname, remarkName=remarkname)[0]
            itchat.send_msg(content, toUserName=friend['UserName'])
        return True
    return False

def warning_meassage_tem_formater(dic):
    return '%s 超出警戒线温度 %s,当前温度为 %s ,请注意控制温度'%(dic['name'],round(dic['degree']-WARNING_TEM_LINE,2),dic['degree'])



