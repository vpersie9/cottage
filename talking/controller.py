__author__ = 'vpersie9'
#-*-coding:utf-8-*-
from flask import Flask,render_template,request
from datetime import datetime
from model import *
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

app=Flask(__name__)
app.secret_key=os.urandom(22)

@app.route('/',methods=['POST','GET'])
def index():
    return u'欢迎来到留言板'

#　下面的路由主要是实现留言的功能
#　显示留言的历史记录
#　添加留言的功能　｀
@app.route('/show',methods=['POST','GET'])
def session():
    all = show()
    if request.method=='POST' and request.args.get('client_id'):
        info=request.form.get('info')
        sender=request.args.get('client_id')
        date_time=datetime.now().strftime('%Y-%m-%d %H:%M')
        send(info,sender,date_time)
        result=show()
        return render_template("show.html",result=result)
    return render_template("show.html",all=all)

if __name__ == "__main__":
    app.run()