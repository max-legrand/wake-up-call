from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from threading import Thread
from twilio.rest import Client
import datetime
import time
import os
from pytz import timezone
app = Flask('')
breakvar = False
tz1 = timezone('US/Pacific')
tz2 = timezone('US/Eastern')
tzswap = 0


@app.route('/')
def home():
    return "I'm alive"


def run():
    try:
        app.run(host='0.0.0.0', port=8080)
    except Exception():
        pass


def keep_alive():
    t = Thread(target=run)
    t.start()


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    global tzswap
    global breakvar
    """Respond to incoming calls with a simple text message."""
    resp = MessagingResponse()
    body = request.values.get('Body', None)
    if body == "BREAK":
        breakvar = True
        print("BREAKVAR = TRUE")
    if body == "GO":
        breakvar = False
        print("BREAKVAR = FALSE")
    if body == "PST":
        tzswap = 0
    if body == "EST":
        tzswap = 1
    try:
        return str(resp)
    except Exception():
        pass


calldays = [0, 1, 2, 3, 4]
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
try:
    print("starting")
    client = Client(account_sid, auth_token)
    keep_alive()
    while 1:
        dayofweek = datetime.datetime.today().weekday()
        if tzswap == 0:
            currentDT = datetime.datetime.now(tz1)
        if tzswap == 1:
            currentDT = datetime.datetime.now(tz2)
        hour = currentDT.hour
        minute = currentDT.minute
        if dayofweek in calldays and hour == 6 and minute == 30 and breakvar is False:
            call = client.calls.create(
                                    url='http://demo.twilio.com/docs/voice.xml',
                                    to=os.getenv("phone1"),
                                    from_=os.getenv("phone2")
                                )
            time.sleep(60)
except Exception:
    pass
