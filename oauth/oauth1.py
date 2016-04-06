# __author__='vpersie9'
# -*-coding:utf-8-*-
# 在生成token的基础上　进行oauth的学习
# 主要是在学习oauth的基本思想　和　具体实现第三方授权登陆的思路
# 本段代码是针对授权码模式下的授权登陆的
# 要学习好授权码实现的流程图　和主要是几个步骤　以及每个步骤所需要的参数


import os
import base64
import random
import time

from flask import Flask, request,redirect

app = Flask(__name__)
app.secret_key=os.urandom(22)

users = {
    "zengxiang": ["jing0123"]
}

redirect_uri='http://localhost:5000/client/passport'
client_id='jing520'
users[client_id]=[]
auth_code={}
oauth_redirect_uri=[]

def gen_token(uid):
    token = base64.b64encode(':'.join([str(uid), str(random.random()), str(time.time() + 7200)]))
    users[uid].append(token)
    return token

def gen_auth_code(uri):
	code=random.randint(0,10000)
	auth_code[code]=uri
	return code

def verify_token(token):
    _token = base64.b64decode(token)
    if users.get(_token.split(':')[0])[-1] == token:
        return 1
    # if float(_token.split(':')[-1]) >= time.time():
    #    return 1
    else:
        return 0

@app.route('/index', methods=['POST', 'GET'])
def index():
    print request.headers
    return 'hello'

@app.route('/login', methods=['POST', 'GET'])
def login():
    uid, pw = base64.b64decode(request.headers['Authorization'].split(' ')[-1]).split(':')
    if users.get(uid)[0] == pw:
        return gen_token(uid)
    else:
        return 'error'

@app.route('/oauth',methods=['POST','GET'])
def oauth():
	if request.args.get('redirect_uri'):
		oauth_redirect_uri.append(request.args.get('redirect_uri'))
	if request.args.get('user'):
		if users.get(request.args.get('user'))[-1]==request.args.get('pwd') and oauth_redirect_uri:
			uri=oauth_redirect_uri[-1]+'?code=%s'%gen_auth_code(oauth_redirect_uri[-1])
			return redirect(uri)
	if request.args.get('code'):
		if auth_code.get(int(request.args.get('code')))==request.args.get('redirect_uri'):
			return gen_token(request.args.get('client_id'))
	return 'please login'

@app.route('/client/login',methods=['POST','GET'])
def client_login():
	uri='http://localhost:5000/oauth?respond_type=code&client_id=%s&redirect_uri=%s'%(client_id,redirect_uri)
	return redirect(uri)

@app.route('/client/passport',methods=['POST','GET'])
def client_passport():
	code=request.args.get('code')
	uri='http://localhost:5000/oauth?grant_type=authorization_code&code=%s&redirect_uri=%s&client_id=%s'%(code,redirect_uri,client_id)
	return redirect(uri)

@app.route('/test', methods=['POST', 'GET'])
def test():
    token = request.args.get('token')
    if verify_token(token):
        return 'data'
    else:
        return 'error'

if __name__ == '__main__':
    app.run(debug=True)

