import json
import subprocess
import time
import requests

while True:
  time.sleep(30)
  url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode=560007&date=08-06-2021"
  res = requests.get(url)
  if not res.ok:
    print "http request failed %s" % res.text
    continue

  for center in res.json()["centers"]:
    for session in center["sessions"]:
      if (session["min_age_limit"] < 45) and (session["available_capacity"] > 0):
        email_ids = ["tom", "kman", "praggu"]
        f = open("email.txt", "w")
        email = "Greeetings and Salutations,\n Appointment available at below "\
                "center: \n\n %s" % json.dumps(center)
        f.write(email)
        for add in email_ids:
          cmd = "sendmail > %s < email.txt" % add
          proc = subprocess.Popen(
             cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
          out, err = proc.communicate()
          if proc.returncode:
            print "Failed to send email because %s" % out
