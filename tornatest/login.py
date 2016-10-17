#-*-coding:utf-8-*-
__author__ = 'vpersie9'

import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop
import os.path
import uuid
import base64
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.options import define,options
define("port",default=5000,help="run on the given port",type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',WelcomeHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler),
        ]

        settings=dict(
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            xsrf_cookies=True,
            login_url="/login"
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        self.set_secure_cookie("username",self.get_argument("username"))
        self.redirect("/")

class WelcomeHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("main_index.html",user=self.current_user)

class LogoutHandler(BaseHandler):
    def get(self):
        # if self.get_argument("logout",None):
        self.clear_cookie("username")
        self.redirect("/")

if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()