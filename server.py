import logic
from flask import *
import json

app = Flask(__name__)



@app.route("/getTakeoffStats")
def get_takeoff_stats():
    mass = request.args.get('mass')
    result = logic.calculate_takeoff_stats(int(mass))
    result_json = {"takeoff_distance": result[logic.TAKEOFF_DISTANCE_CELL], "takeoff_time": result[logic.TAKEOFF_TIME_CELL]}
    
    result_json["overweight_mass"] = result[logic.OVERWEIGHT_MASS_CELL] if len(result) > 2 else None
    return json.dumps(result_json)
     


@app.route("/")
def index():
    return 'Test'

if __name__ == '__main__':
    app.run("0.0.0.0", 8080, debug=True)