#!/usr/bin/python3

import requests
import json
import os
import time
import os
import sys
from twilio.rest import Client

print(sys.argv)
if (sys.argv[-1] == "--help" or len(sys.argv) == 1):
	print("USAGE: script.py RECIPIENT_1 [RECIPIENT_2 ...]")
	exit(0)


dates = ["04-05-2021", "11-05-2021", "18-05-2021", "25-05-2021", "01-06-2021",
    "08-06-2021", "15-06-2021", "22-06-2021", "29-06-2021"]
centres = ["294", "265"]

account_sid = 'SID' # replace this 
auth_token = 'TOKEN' # replace this
client = Client(account_sid, auth_token)

while(1):

	for d in dates:
		for c in centres:
			url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + c + "&date=" + d
			res = requests.get(url)
			if not res.ok:
				print ("http request failed %s" % res.text)
				continue
			for center in res.json()["centers"]:
				for session in center["sessions"]:
					if ( 
              session["min_age_limit"] < 45 and session["available_capacity"] > 0 ):
						text = center["name"] + " " + center["address"] + " " \
                +  session["date"] + " capacity: ", session["available_capacity"]

						# print(text)
						for recipient in sys.argv[1:]:
							message = client.messages.create(
                  body=text,
                  from_='+17272025536',
                  to=recipient
                  )

	print("Checking again in 60 seconds")
	time.sleep(60)
