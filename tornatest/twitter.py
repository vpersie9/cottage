#-*-coding:utf-8-*-
__author__ = 'vpersie9'

import tornado.web
import tornado.httpserver
import tornado.auth
import tornado.options
import tornado.ioloop
import os.path
import functools
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
            (r'/',TwitterHandler),
            (r'/logout',LogoutHandler),
        ]

        settings=dict(
            twitter_consumer_key="cWc3 ... d3yg",
            twitter_consumer_secret="nEoT ... cCXB4",
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
        )

        tornado.web.Application.__init__(self,handlers,**settings)

class TwitterHandler(tornado.web.RequestHandler,tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        oAuthToken=self.get_secure_cookie("oauth_token")
        oAuthSecret=self.get_secure_cookie("oauth_secret")
        userID=self.get_secure_cookie("user_id")

        if self.get_argument("oaut_token",None):
            self.get_authenticated_user(functools.partial(self._twitter_on_auth))
            return

        elif oAuthToken and oAuthSecret:
            accessToken={
                'key':oAuthToken,
                'secret':oAuthSecret
            }
            self.twitter_request(
                '/users/show',
                access_token=accessToken,
                user_id=userID,
                callback=functools.partial(self._twitter_on_user)
            )
            return

        self.authorize_redirect()

    def _twitter_on_auth(self,user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500, "Twitter authentication failed")

        self.set_secure_cookie('user_id',str(user['id']))
        self.set_secure_cookie('oauth_token',user['access_token']['key'])
        self.set_secure_cookie('oauth_secret',user['access_token']['secret'])
        self.redirect('/')
        self.finish()

    def _twitter_on_user(self,user):
        if not user:
            self.clear_all_cookies()
            raise tornado.web.HTTPError(500,"Couldn't retrieve user information")

        self.render('home.html',user=user)

class LogoutHandler(tornado.web.RequestHandler):
    def get(self):
        self.clear_all_cookies()
        self.render("logout.html")


if __name__=="__main__":
    tornado.options.parse_command_line()
    http_server=tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()