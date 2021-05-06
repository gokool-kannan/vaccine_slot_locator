#!/usr/bin/python3

import requests
import json
import time
import os
import sys
from twilio.rest import Client

a = sys.argv
na = len(a)

print(a)

if (
    a[-1] == "--help"
    or na < 3
    or (a[1] != "console" and a[1] != "sms")
    or (a[1] == "sms" and na < 4)
):
    print(
        "USAGE: script.py console|sms YOUR_STATE RECIPIENT_1 [RECIPIENT_2 RECIPIENT_3...]"
    )
    exit(0)


states = (
    "Andaman And Nicobar Islands",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chandigarh",
    "Chhattisgarh",
    "Dadra And Nagar Haveli",
    "Delhi",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu And Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Ladakh",
    "Lakshadweep",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Puducherry",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
    "Daman And Diu",
)


def get_districts(state):
    i = 1

    for s in states:
        if s == state:
            break
        i = i + 1

    url = "http://cdn-api.co-vin.in/api/v2/admin/location/districts/" + str(i)
    res = requests.get(url)
    i = 0
    districts = []
    # print(res)
    for d in res.json()["districts"]:
        districts.append(d["district_id"])
    return districts


state = a[2]
districts = get_districts(state)
# districts = [294, 265]

print("Districts IDs are: ", districts)

dates = [
    "05-05-2021",
    "12-05-2021",
    "19-05-2021",
    "26-05-2021",
    "02-06-2021",
    "09-06-2021",
    "16-06-2021",
    "23-06-2021",
    "30-06-2021",
]


account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]
client = Client(account_sid, auth_token)

while 1:
    for d in dates:
        for district in districts:
            url = (
                "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="
                + str(district)
                + "&date="
                + d
            )
            res = requests.get(url)
            if not res.ok:
                print("http request failed %s" % res.text)
                continue
            for center in res.json()["centers"]:
                for session in center["sessions"]:
                    if (
                        session["min_age_limit"] != 45
                        and session["available_capacity"] != 0
                    ):
                        text = (
                            center["name"]
                            + " "
                            + center["district_name"]
                            + " "
                            + session["date"]
                            + " capacity: "
                            + str(session["available_capacity"])
                        )
                        if a[1] == "console":
                            print(text)
                        elif a[1] == "sms":
                            for recipient in a[3:]:
                                message = client.messages.create(
                                    body=text, from_="+17272025536", to=recipient
                                )
            time.sleep(2)
