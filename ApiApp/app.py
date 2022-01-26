from flask import Flask, render_template, request, session, redirect
from datetime import datetime
import json
import requests

app = Flask(__name__)
app.config["SECRET_KEY"] = "az7e89r"
jsonObj = open('./config.json')
cfg = json.load(jsonObj)
apiKey = cfg["wApiKey"]


@app.route('/', methods=['GET', 'POST'])
def index():
    meteo_data, name, dtobject, error, country = "", "", "", "", ""
    if request.method == 'POST':
        data = request.form['city']
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={data}&limit=5&appid={apiKey}")
        if (json.loads(response.text) == []):
            error = "1"
        else:
            name = json.loads(response.text)[0]["name"]
            country = json.loads(response.text)[0]["country"]
            lat = json.loads(response.text)[0]["lat"]
            lon = json.loads(response.text)[0]["lon"]
            meteo_res = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&lang=fr&units=metric&appid={apiKey}")
            meteo_data = json.loads(meteo_res.text)
            dtobject = datetime.fromtimestamp(meteo_data['current']['dt'])
            
        
    if request.method == 'GET':
        response = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q=Paris&limit=5&appid={apiKey}")
        name = json.loads(response.text)[0]["name"]
        country = json.loads(response.text)[0]["country"]
        lat = json.loads(response.text)[0]["lat"]
        lon = json.loads(response.text)[0]["lon"]
        meteo_res = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,hourly,daily&lang=fr&units=metric&appid={apiKey}")
        meteo_data = json.loads(meteo_res.text)
        dtobject = datetime.fromtimestamp(meteo_data['current']['dt'])
    return render_template('home.html', data=meteo_data, city=name, date=dtobject, error=error, country=country)