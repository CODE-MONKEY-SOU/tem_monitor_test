#-*- coding: UTF-8 -*-
from flask_apscheduler import APScheduler
from flask_login import login_required, login_user, logout_user, current_user,LoginManager
from flask import (Flask, render_template, redirect, url_for, request, flash)
from form import *
import business
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import json
from model_ora import *
import threading
import itchat


app = Flask(__name__)
app.config.from_object('config')
scheduler = APScheduler()

# bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "show_login"
login_manager.session_protection = "strong"
db = SQLAlchemy(app)


@app.route('/index.html', methods=['GET'])
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
@login_required
def show_index():
    return render_template('index.html')


@app.route('/login', methods=['GET'])
def show_login():
    form = LoginForm()
    return render_template('login.html',form=form,unicode='utf-8')


@app.route('/login', methods=['POST'])
def login_acion():
    if business.login_process({'username':request.form['username'],'password':request.form['password']}):
        return redirect(request.args.get('next') or url_for('show_index'))
    else:
        return redirect(url_for('show_login'))

@app.route('/logout',methods=['GET'])
@login_required
def logout_action():
    logout_user()
    return redirect(url_for('show_login'))


@app.route('/upload', methods=['POST'])
def upload_action():
    jsondata = request.get_data()
    dic = json.loads(jsondata)
    print(business.upload_process(dic))
    return "ok"


@app.route('/query', methods=['POST'])
def query_action():
    # dic = dict(request.json)
    dic = request.form.to_dict()
    # print(jsondata)
    # dic = json.loads(jsondata)
    if dic['qtype']=='history':
        return json.dumps({'device_info': business.query_device_process(dic), 'tem_info': business.query_tem_process(dic)})
    elif dic['qtype']=='current':
        return json.dumps({'device_info': business.query_device_process(dic), 'tem_info': business.query_tem_current_process(dic)})
    elif dic['qtype']=='deviceslist':
        return json.dumps({'devicelist': business.query_device_list_process()})



@app.route('/page_ssjc',methods=['GET'])
def show_ssjc():
    return render_template('ssjc.html')


@app.route('/page_<pagename>',methods=['GET'])
def show_page(pagename):
    pagename=pagename+'.html'
    return render_template(pagename)


@login_manager.user_loader
def load_user(user_id):
    return BaseUser.query.filter_by(id=str(user_id)).first()



def wechatthread():
    itchat.auto_login(hotReload=True)
    #     # itchat.auto_login()
    itchat.run()




if __name__ == '__main__':
    # itchat.auto_login(hotReload=True)
    # #     # itchat.auto_login()
    # itchat.run()

    # t = threading.Thread(target=wechatthread)
    # t.setDaemon(True)
    # t.start()

    # scheduler.init_app(app)
    # scheduler.start()
    app.run()


