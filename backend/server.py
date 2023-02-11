import logic as logic
from flask import *
from flask_cors import cross_origin
from json import *
from pymongo import MongoClient
import requests

WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"

MIN_TAKEOFF_TEMP = 15
MAX_TAKEOFF_TEMP = 30

app = Flask(__name__)

MONGO_URI = r"mongodb://localhost:27017/"
TAKEOFF_STATS_DB = "takeoff_stats"
STATS_COLLECTION = "stats"

client = MongoClient(MONGO_URI)

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

    result = {"takeoff_distance": takeoff_stats[logic.TAKEOFF_DISTANCE_CELL], "takeoff_time": takeoff_stats[logic.TAKEOFF_TIME_CELL]}

    result.update({"overweight_mass": takeoff_stats[logic.OVERWEIGHT_MASS_CELL]}) if len(takeoff_stats) > 2 else None

    json_result = dumps(result)
    save_stats(mass, result)
    return json_result
     

def save_stats(mass, takeoff_stats):
    """Helper function that recieves data and saves it to the stats collection
    Args:
        mass (float): the mass to save
        takeoff_stats (dict): the takeoff stats to save in the db
    Returns:
        None
    """
    db = client[TAKEOFF_STATS_DB]
    collection = db[STATS_COLLECTION]
    
    takeoff_stats["mass"] = mass
    
    collection.insert_one(takeoff_stats)

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

if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)