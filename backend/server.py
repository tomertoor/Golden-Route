import logic as logic
from flask import *
from flask_cors import cross_origin
from json import *
from pymongo import MongoClient
import requests

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


def check_date_location(date, location):
    

if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)