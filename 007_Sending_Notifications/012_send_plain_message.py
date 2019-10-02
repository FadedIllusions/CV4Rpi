# Usage
# python 012_send_plain_message.py --conf config/config.json


# Import Needed Packages
from helpers.notifications import TwilioNotifier
from helpers.utils import Conf
import argparse


# Construct Argument Parser And Parse Arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True, help="Path To Input Configuration File")
args = vars(ap.parse_args())


# Load Configuration File And Init Twilio Notifier
conf = Conf(args["conf"])
tn = TwilioNotifier(conf)

# Send Text Message
print("[INFO] Sending SMS Message...")
tn.send("Incoming Message From Your RPi!")
print("[INFO] SMS Message Sent.")