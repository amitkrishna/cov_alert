#Import Libraries
import requests
import json
import time
import datetime
import smtplib

#Write a loop which checks for every 1000 seconds
while True:
    #Define Constants
    PINCODE = str(input("Enter the PINCODE?"))  # Example 600040
    MY_EMAIL = str(input("ENTER YOUR EMAIL ID"))  # From this mail id, the alerts will be sent
    MY_DOMAIN = str(input("Enter mailgun domain name"))
    MY_MAIL = str(input("Enter mailgun sandbox id"))
    MY_API = "API_KEY"  # Enter api key for mailgun 

    today = time.strftime("%d/%m/%Y")
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={PINCODE}&date={today}"


    #Start a session
    with requests.session() as session:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        _response = session.get(url, headers=headers)

        #Receive the response
        response = _response.json()
        for center in response['centers']:
            for session in center['sessions']:
                #For Age not equal to 45 and capacity is above zero
                if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                    message_string=f"Hej: {today}'s Alert'!! \n\n Available Slots - {session['available_capacity']} in center {center['name']} on the session {session['date']} for the minimum age {session['min_age_limit']}"
                    send_simple_message(MY_EMAIL, MY_DOMAIN, MY_MAIL, message_string)
        time.sleep(1000)


def send_simple_message(MY_EMAIL, MY_DOMAIN, MY_MAIL, message_string):
	return requests.post(
            f"https://api.mailgun.net/v3/{MY_DOMAIN}/messages",
          		auth=("api", MY_API),
          		data={"from": f"{MY_MAIL}",
                            "to": [MY_EMAIL],
                            "subject": "Alert on Covid 19 Vaccination",
                            "text": message_string})

