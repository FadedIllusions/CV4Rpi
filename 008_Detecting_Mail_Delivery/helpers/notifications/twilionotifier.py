# Import Needed Packages
from twilio.rest import Client

class TwilioNotifier:
	def __init__(self, conf):
		# Store Configuration Object
		self.conf = conf
		
	def send(self, msg):
		# Init Twilio Client And Send Message
		client = Client(self.conf["twilio_sid"], self.conf["twilio_auth"])
		client.messages.create(to=self.conf["twilio_to"], from_=self.conf["twilio_from"], body=msg)