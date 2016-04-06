# this is just a little test
import random
def function(arg):
	def gunction(args):
		print arg+args
	return gunction

if __name__=='__main__':
	function(random.random())(random.random())
