import logic as logic
from flask import *
from flask_cors import cross_origin
from json import *

import db_handler


import weather

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
        takeoff_stats = logic.calculate_takeoff_stats(int(mass)) # For runtime efficiency, I didn't try to query the db to check for similar times as it is easier to calculate it in this function
    except:
        return "Error, unexpected input", 504

    result = {"takeoff_distance": takeoff_stats[logic.TAKEOFF_DISTANCE_CELL], "takeoff_time": takeoff_stats[logic.TAKEOFF_TIME_CELL], "overweight_mass": takeoff_stats[logic.OVERWEIGHT_MASS_CELL]}

    
    json_result = dumps(result)
    db_handler.save_stats(mass, takeoff_stats[logic.TAKEOFF_DISTANCE_CELL], takeoff_stats[logic.TAKEOFF_TIME_CELL], takeoff_stats[logic.OVERWEIGHT_MASS_CELL])
    
    return json_result


@app.route("/checkTakeoffTime")
@cross_origin()
def check_takeoff_time():
    """Flask handler for checktakeoff time

    Returns:
        List: list represnting the hours which you can takeoff at
    """
    date = request.args.get("date")
    location = {"longitude": 35, "latitude": 30} # default values that are written in the instructions
    timezone = request.args.get("timezone")
    return weather.check_date_location(location, timezone, date)



def start():
    db_handler.create_db()
    return app