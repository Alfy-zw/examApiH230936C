from flask import Flask, render_template, request 
from datetime import datetime

import time

import re
  
# import json to load JSON data to a python dictionary 
import json 
  
# urllib.request to make a request to api 
import urllib.request 
  
app = Flask(__name__) 
  
@app.route('/', methods =['POST', 'GET']) 
def weather(): 
    if request.method == 'POST': 
        city = request.form['city'] 
    else: 
        # for default name harare 
        city = 'Harare'

    cities = split_list = re.split(r'[ ,\-]+', city)
    cities = [item.strip() for item in cities if item.strip()]

    # your API key will come here 
    api = "61d8f5550ef820beb3ec1986c93a2841" 

    #Define variables
    cities_data = []
    error = None

    try:
        for city in cities:
            # source contain json data from api 
            source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api).read() 
            
            # converting JSON data to a dictionary 
            list_of_data = json.loads(source)
        
            # data for variable list_of_data 
            data = { 
                "country_code": str(list_of_data['sys']['country']), 
                "temp": round(float(list_of_data['main']['temp']) - 273.15),
                "humidity": round(float(list_of_data['main']['humidity'])),
                "wind_speed": float(list_of_data['wind']['speed']), 
                "description": str(list_of_data['weather'][0]['description']),
                "city_name": str(list_of_data['name']),
            } 

            # Append data for current city to cities_data list
            cities_data.append(data)
    except Exception as e:
        error = e

    return render_template('index.html',error = error, cities_data = cities_data) 

@app.route('/forecast', methods =['POST', 'GET']) 
def forecast(): 
    if request.method == 'POST': 
        city = request.form['city'] 
    else: 
        # for default name harare 
        city = 'Harare'

    # your API key will come here 
    api = "61d8f5550ef820beb3ec1986c93a2841" 

    #Define variables
    days = []
    temps = []
    windspeed = []
    error = None

    try:
        # source contain json data from api 
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?q=' + city + '&appid=' + api).read() 
           
        # converting JSON data to a dictionary 
        list_of_data = json.loads(source)
        forecast_data = list_of_data['list']
        for data in forecast_data:
            temps.append(round(float(data['main']['temp']) - 273.15))
            windspeed.append(round(float(data['wind']['speed'])))
            dt_txt = str(data['dt_txt'])
            # Extract components from dt_txt
            date_part, time_part = dt_txt.split()

            # Get short day name
            short_day_name = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][datetime.strptime(date_part, "%Y-%m-%d").weekday()]

            # Construct formatted string with short day name and time in 24-hour format
            datelo = f"{short_day_name} {time_part[:5]}"
            days.append(datelo)
    except Exception as e:
        error = e

    return render_template('forecast.html',error = error, temps = temps, windspeed = windspeed, days = days) 
  
  
  
if __name__ == '__main__': 
    app.run(host="0.0.0.0",port=3000,debug = True) 
