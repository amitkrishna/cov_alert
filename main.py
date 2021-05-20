import requests
import json
import time
import datetime
import smtplib

pinCODE = str(input("Enter the PINCODE?"))
myEMAIL = str(input("ENTER YOUR EMAIL ID"))
myDOMAIN = str(input("Enter mailgun domain name"))
myMAIL = str(input("Enter mailgun sandbox id"))
myAPI = "MAILGUN_API_KEY"
minAGE = str(input("Enter minimum age for Vaccination"))
msgStr = ""


def send_simple_message(MY_EMAIL, MY_DOMAIN, MY_MAIL, message_string):
	return requests.post(
            f"https://api.mailgun.net/v3/{MY_DOMAIN}/messages",
          		auth=("api", MY_API),
          		data={"from": f"{MY_MAIL}",
                            "to": [MY_EMAIL],
                            "subject": "Alert on Covid 19 Vaccination",
                            "text": message_string})

while True:
    toDay = time.strftime("%d/%m/%Y")
    _url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pinCODE}&date={toDay}"


    #Start a session
    with requests.session() as session:
        _headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        _response = session.get(_url, headers=_headers)

        response = _response.json()
        for center in response['centers']:
            for session in center['sessions']:
                if (session['min_age_limit'] != minAGE) & (session['available_capacity'] > 0):
                    msgStr+=f"Hej: {toDay}'s Alert'!! \n\n Available Slots - {session['available_capacity']} in center {center['name']} on the session {session['date']} for the minimum age {session['min_age_limit']}"
        
    send_simple_message(myEMAIL, myDOMAIN, myMAIL, msgStr)
time.sleep(1000)
