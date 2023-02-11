import logic as logic
from flask import *
from flask_cors import cross_origin
from json import *

import db_handler

import requests

WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"

MIN_TAKEOFF_TEMP = 15
MAX_TAKEOFF_TEMP = 30

app = Flask(__name__)

TAKEOFF_STATS_DB = "takeoff_stats"
STATS_COLLECTION = "stats"



@app.route("/getTakeoffStats")
@cross_origin()
def get_takeoff_stats():
    """Flask GET response that processes the user sending the mass and returns data. Saves it in the mongodb aswell
    Args:
        In the HTTP request it sends mass. (int)
    Returns:
        HTTP GET Response JSON of the takeoff stats
    """

    
    mass = request.args.get('mass')
    try:
        mass = int(mass)
    except:
        return "Error, wrong input type!", 504
    try:
        takeoff_stats = logic.calculate_takeoff_stats(int(mass))
    except:
        return "Error, unexpected input", 504

    result = [takeoff_stats[logic.TAKEOFF_DISTANCE_CELL], takeoff_stats[logic.TAKEOFF_TIME_CELL]]

    
    json_result = dumps(result)
    db_handler.save_stats(mass, takeoff_stats[logic.TAKEOFF_DISTANCE_CELL], takeoff_stats[logic.TAKEOFF_TIME_CELL], )
    return json_result


@app.route("/checkTakeoffTime")
@cross_origin()
def check_takeoff_time():
    date = request.args.get("date")
    location = {"longitude": 35, "latitude": 30} # default values that are written in the instructions
    timezone = request.args.get("timezone")
    
    return check_date_location(location, timezone, date)



def check_date_location(location, timezone, date="2023-1-1"):
    temperature_list = get_weather_temp(date, location["longitude"], location["latitude"], timezone)
    result = {}
    for hour, temp in enumerate(temperature_list):
        if MAX_TAKEOFF_TEMP > temp > MIN_TAKEOFF_TEMP:
            result[hour] = True
        else:
            result[hour] = False
    return result

def get_weather_temp(date, longtitude, latitude, timezone="auto"):
    """Perform a rest api request to the open meteo api and returns a list of the temperature at each hour

    Args:
        date (string): the date
        longtitude (float): longtitude
        latitude (float): latitude
        timezone (str, optional): the timezone. Defaults to "auto".
    Returns: 
        temperatures of each hour in the day
    """
    response = requests.get(WEATHER_API, params={'longitude': longtitude, 'latitude': latitude, 'hourly': "temperature_2m", 'timezone': timezone, 'start_date': date, 'end_date': date})    
    data = response.json()
    print(data)
    return data["hourly"]["temperature_2m"]

def main():
    db_handler.create_db()
    app.run("0.0.0.0", 8080, debug=True)

if __name__ == '__main__':
    main()