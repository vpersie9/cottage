#-*-coding:utf-8-*-
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import os.path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from tornado.options import define,options

define("port",default=9000,help="run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r'/',HelloHandler)]
		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__),'templates'),
			ui_modules={"Hello":HelloModule},
			debug=True,)
		tornado.web.Application.__init__(self,handlers,**settings)

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('hello.html')

class HelloModule(tornado.web.UIModule):
	def render(self):
		return "<h1>Hello,World!</h1>"

if __name__=="__main__":
	tornado.options.parse_command_line()
	httpserver=tornado.httpserver.HTTPServer(Application())
	httpserver.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
		
