import os
from dotenv import load_dotenv
import requests
from twilio.rest import Client

load_dotenv("codes.env")

owm_api_key = os.getenv('OWM_API_KEY')
account_sid = os.getenv('ACCOUNT_SID')
auth_token = os.getenv('AUTH_TOKEN')

parameters = {
    "lat": -33.918861,
    "lon": 18.423300,
    "formatted": 0,
    "cnt": 4,
}

response = requests.get(
    "http://api.openweathermap.org/data/2.5/forecast",
    params={**parameters, "appid": owm_api_key},
)
response.raise_for_status()
weather_data = response.json()

will_rain = False
for forecast in weather_data["list"]:
    weather_id = forecast["weather"][0]["id"]
    if weather_id < 700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        messaging_service_sid="MGcc344b21de6d7ca6d6421decb7393f45",
        body="It's going to rain today. Don't forget to bring an Umbrella.",
        to="+27618580714"
    )
    print(message.status)
