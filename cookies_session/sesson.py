#-*-coding:utf-8-*-
from flask import Flask,session,redirect,url_for,escape,request
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#该脚本流程和同目录下cookies.py 相同　只不过是cookies 和　session 两种不同的实现方式

app=Flask(__name__)
app.secret_key=os.urandom(22)

@app.route('/')
def index():
	if 'login' in session:
		return 'logged in as %s'%escape(session['login'])
	return 'you are not logged in'

@app.route('/login',methods=['POST','GET'])
def login():
	if 'login' in session:
		return redirect(url_for('index'))
	if request.method=='POST':
		session['login']=request.form['username']
		return redirect(url_for('index'))

	return '''
		<form action='' method="post">
		<p><input type=text name=username />
		<p><input type=submit value=login />
		</form>
		'''

@app.route('/logout')
def logout():
	session.pop('login',None)
	return redirect(url_for('index'))

if __name__=="__main__":
	app.run()
