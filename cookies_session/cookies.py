__author__ = 'vpersie9'
#-*-coding:utf-8-*-
from flask import Flask,make_response,redirect,url_for,escape,request
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app=Flask(__name__)
app.secret_key=os.urandom(22)

#主页路由　登录注销都是最终定向到这个路由
@app.route('/')
def index():
    if request.cookies.get('login'):
        return 'logged in as %s'%escape(request.cookies['login'].split('_')[0])
    return 'you are not logged in'

#登陆路由
@app.route('/login',methods=['POST','GET'])
def login():
    if request.cookies.get('login'):
        return redirect(url_for('index'))
    if request.method=='POST':
        resp=make_response(redirect(url_for('index')))
#将cookie的设置加上时间　当然也可以通过hamc 加密算法对cookie进行加密签名　但是这里就简单的设置一下
        resp.set_cookie('login', '_'.join([request.form.get('username'), str(time.time()+600)]))
        return resp
    return '''<form action='' method="post">
                <p><input type=text name=username />
                <p><input type=submit value=login />
              </form>
                '''
#注销路由　因为flask好像没有对cookie删除的方法　这里对login　cookie重新设置　并让他的生命周期为零　这样就相当于删除了cookie
#可以类比与flask 会话功能session.pop('login',None)  这里的session是有删除方法的
@app.route('/logout')
def logout():
    resp=make_response(redirect(url_for('index')))
    resp.set_cookie('login','',expires=100)
    return resp

if __name__=="__main__":
    app.run(port=8000,debug=True)
