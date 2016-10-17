#-*-coding:utf-8-*-
__author__ = 'vpersie9'
import os.path
import tornado.options
import tornado.web
import tornado.httpserver
import tornado.ioloop
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
            (r'/',MainHandler),
            (r'/purchase',PurchaseHandler),
                  ]
        settings=dict(
            debug=True,
            cookie_secret=base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes),
            xsrf_cookies=True,
            template_path=os.path.join(os.path.dirname(__file__),"templates"),
            static_path=os.path.join(os.path.dirname(__file__),"static"),
        )
        tornado.web.Application.__init__(self,handlers,**settings)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        cookie=self.get_secure_cookie("count")
        if cookie:
            count=int(cookie)+1
        else:
            count=1
        if count==1:
            countString="1 time"
        else:
            countString="%d times" %count
        self.set_secure_cookie("count",str(count))
        self.write(
            '<html><head><title>Cookie Counter</title></head>'
            '<body><h1>You have viewed this page %s times.</h1>' %countString+
            '</body></html>'
        )

class PurchaseHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("xsrf.html")

    def post(self):
        title=self.get_argument("title")
        quantity=self.get_argument("quantity")
        if title and quantity:
            self.write(title+ ' ' + ' '+quantity)

if __name__=="__main__":
    tornado.options.parse_command_line()
    httpserver=tornado.httpserver.HTTPServer(Application())
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()