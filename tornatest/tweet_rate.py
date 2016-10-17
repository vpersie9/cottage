#-*-coding:utf-8-*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from tornado.options import define,options
define("port",default=9000,help="run on the given port",type=int)

class Application(tornado.web.Application):
	def __init__(self):
		handlers=[(r"/",IndexHandler)]
		settings=dict(debug=True,)
		tornado.web.Application.__init__(self,handlers,**settings)
		
class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		query=self.get_argument('q')
		client=tornado.httpclient.HTTPClient()
		response=client.fetch("http://search.twitter.com/search.json?"+urllib.urlencode({'q':query,"result_type":"recent","rpp":100}))
		body=json.loads(response.body)
		result_count=len(body["results"])
		now=datetime.datetime.utcnow()
		raw_oldest_tweet_at=body["results"][-1]['created_at']
		oldest_tweet_at=datetime.datetime.strptime(raw_oldest_tweet_at,"%a, %d %b %Y %H:%M%S +0000")
		seconds_diff=time.mktime(now.timetuple())-time.mktime(oldest_tweet_at.timetuple())
		tweets_per_second=float(result_count)/seconds_diff
		self.write("""
			<div style="text-align:center">
				<div style="font-size: 72px">%s</div>
				<div style="font-size: 144px">%.02f</div>
				<div style="font-size: 24px">tweets per second</div>
			</div>"""%(query,tweets_per_second))

if __name__=="__main__":
	tornado.options.parse_command_line()
	http_server=tornado.httpserver.HTTPServer(Application())
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
