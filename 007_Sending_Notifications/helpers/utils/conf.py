# Import Needed Packages
from json_minify import json_minify
import json

class Conf:
	def __init__(self, confPath):
		# Load And Store Configuration And Update Objects Dictionary
		conf = json.loads(json_minify(open(confPath).read()))
		self.__dict__.update(conf)
		
	def __getitem__(self, k):
		# Return Value Associated With Supplied Key
		return self.__dict__.get(k, None)