#-*-coding:utf-8-*-

import os.path
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.escape
import json
import functools
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define,options
define("port",default=8080,help="run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r'/',IndexHandler),(r'/chat',ChatHandler)]
		settings=dict(
				template_path=os.path.join(os.path.dirname(__file__),"templates"),
				static_path=os.path.join(os.path.dirname(__file__),"static"),
				debug=True,
			)
		tornado.web.Application.__init__(self,handlers,**settings)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.write(u'你好主任 我是主页君！')

class ChatHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('chat.html')

	@tornado.web.asynchronous
	def post(self):
		name=self.get_argument('name')
		password=self.get_argument('password')
		if name!="zengxiang" or password!="jing0123":
			self.write(tornado.escape.json_encode({'warning':u"用户名或者密码错误！"}))
		if name=="zengxiang" and password=="jing0123":
			self.write(json.dumps({'login_success':u"登录成功！"}))
		self.finish()

if __name__=="__main__":
	tornado.options.parse_command_line()
	httpserver=tornado.httpserver.HTTPServer(Application())
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
