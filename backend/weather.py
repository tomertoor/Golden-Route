import requests
from datetime import datetime

ARCHIVE_WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"
FORECAST_WEATHER_API = "https://api.open-meteo.com/v1/forecast"

MIN_TAKEOFF_TEMP = 15
MAX_TAKEOFF_TEMP = 30

WEEK_TIME = 7


def check_date_location(location, timezone, date="2023-1-1"):
    """Handles checking if at a specfic date and location viable it what hours for takeoff

    Args:
        location (dict): Dictionary representing the location
        timezone (str): The timezone of the area to fetch from (for some reason it is relevant for the api)
        date (str, optional): the date to get the weather for. Defaults to "2023-1-1".

    Returns:
        list: List that each index represents an hour and if it is possible to takeoff at that hour
    """
    temperature_list = get_weather_temp(date, location["longitude"], location["latitude"], timezone)
    
    result = []
    for temp in temperature_list:
        if MAX_TAKEOFF_TEMP > temp > MIN_TAKEOFF_TEMP:
            result.append(True)
        else:
            result.append(False)
            
    return result

def get_weather_temp(date, longtitude, latitude, timezone="auto"):
    """Perform a rest api request to the open meteo api and returns a list of the temperature at each hour. Becuase openmeteo archive api doesn't give results if the date is less than 7 days or if it is in the future, performs request to forecast
    Args:
        date (string): the date
        longtitude (float): longtitude
        latitude (float): latitude
        timezone (str, optional): the timezone. Defaults to "auto".
    Returns: 
        temperatures of each hour in the day
    """
    
    current_time = datetime.today()
    desired_date = datetime.strptime(date, "%Y-%m-%d")
    day_difference = (current_time - desired_date).days
    
    if day_difference > WEEK_TIME: #if the date happend before the last 7 day then its a query for archive, if it happend in the past week or in the next week its for the forecast
        response = requests.get(ARCHIVE_WEATHER_API, params={'longitude': longtitude, 'latitude': latitude, 'hourly': "temperature_2m", 'timezone': timezone, 'start_date': date, 'end_date': date})    
        data = response.json()
        
        return data["hourly"]["temperature_2m"]
    
    else:
        response = requests.get(FORECAST_WEATHER_API, params={'longitude': longtitude, 'latitude': latitude, 'hourly': "temperature_2m", 'timezone': timezone, 'past_days': WEEK_TIME})    
        data = response.json()
        time_indexes = data["hourly"]["time"]


        date_indexes = [key for key, value in enumerate(time_indexes) if date in value] #gets a list of all the releveant
        
        return data["hourly"]["temperature_2m"][date_indexes[0]:date_indexes[-1]+2]
    
    
