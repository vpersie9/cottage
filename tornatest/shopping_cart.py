#-*-coding:utf-8-*-
import tornado.web
import tornado.options
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
from uuid import uuid4
import functools
import os.path
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class ShoppingCart(object):
	totalInventory=10
	callbacks=[]
	carts={}

	def register(self,callback):
		self.callbacks.append(callback)

	def moveItemToCart(self,session):
		if session in self.carts:
			return 

		self.carts[session]=True
		self.notifyCallbacks()
	
	def removeItemFromCart(self,session):
		if session not in self.carts:
			return

		del(self.carts[session])
		self.notifyCallbacks()
	
	def notifyCallbacks(self):
		for c in self.callbacks:
			self.callbackHelper(c)
	
		self.callbacks=[]
	
	def callbackHelper(self,callback):
		callback(self.getInventoryCount())
	
	def getInventoryCount(self):
		return self.totalInventory-len(self.carts)


class DetailHandler(tornado.web.RequestHandler):
	def get(self):
		session=uuid4()
		count=self.application.shoppingCart.getInventoryCount()
		self.render("long.html",session=session,count=count)

class CartHandler(tornado.web.RequestHandler):
	def post(self):
		action=self.get_argument('action')
		session=self.get_argument('session')
		if not session:
			self.set_status(400)
			return

		if action=="add":
			self.application.shoppingCart.moveItemToCart(session)
		elif action=="remove":
			self.application.shoppingCart.removeItemFromCart(session)
		else:
			self.set_status(400)

class StatusHandler(tornado.websocket.WebSocketHandler):
	@tornado.web.asynchronous
	def get(self):
		self.application.shoppingCart.register(functools.partial(self.on_message))

	def on_message(self,count):
		self.write('{"inventoryCount":"%d"}'%count)
		self.finish()

class Application(tornado.web.Application):
	def __init__(self):
		self.shoppingCart=ShoppingCart()
		handlers=[
			(r'/',DetailHandler),
			(r'/cart',CartHandler),
			(r'/cart/status',StatusHandler)
		]

		settings=dict(
			template_path=os.path.join(os.path.dirname(__file__),"templates"),
			static_path=os.path.join(os.path.dirname(__file__),"static"),
		)
			
		tornado.web.Application.__init__(self,handlers,**settings)
		
if __name__=="__main__":
		tornado.options.parse_command_line()
		app=Application()
		httpserver=tornado.httpserver.HTTPServer(app)
		httpserver.listen(8080)
		tornado.ioloop.IOLoop.instance().start()
