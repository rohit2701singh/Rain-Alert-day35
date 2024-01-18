import requests
from twilio.rest import Client
import datetime as dt
import os

api_key = os.environ.get("OPEN_WEATHER_API_KEY")
account_sid = os.environ.get("ACCOUNT_SID_TWILIO")
auth_token = os.environ.get("AUTH_TOKEN_TWILIO")

parameters = {
    "lat":  25.3167,
    "lon": 51.4667,
    "appid": api_key,
    "exclude": "current,minutely,daily",
}

response = requests.get(url="https://api.openweathermap.org/data/2.8/onecall", params=parameters)
response.raise_for_status()
weather_data = response.json()
time_zone = weather_data["timezone"]
# print(weather_data)
print(f"your time zone: {time_zone}")

hourly_weather_slice_data = weather_data["hourly"][0:12]

weather_info = []
will_rain = False

for hour_data in hourly_weather_slice_data:
    weather_id = hour_data["weather"][0]["id"]
    if int(weather_id) < 700:
        # change unix datetime to current datetime for particular timezone.
        get_date_time = dt.datetime.fromtimestamp(int(hour_data["dt"]))
        get_time = get_date_time.time().strftime('%I:%M %p')  # get only time in 12 hours format
        description = hour_data["weather"][0]["description"]

        weather_info.append(f"{get_time} : {description}")
        will_rain = True
print(weather_info)

if will_rain:   # send sms using twilio
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Don't forget to bring an umbrella☔. Details:\ntimezone: {time_zone}\n\n{weather_info}",
        from_='+125xxxxxxx',
        to='+91xxxxxx'
    )
    print(message.status)
