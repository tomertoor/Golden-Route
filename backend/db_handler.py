import sqlite3


try:
    connection = sqlite3.connect("./goldenroute.db", check_same_thread=False)
    cur = connection.cursor()
except:
    print("SQL isn't working")

def create_db():
    """Creates the database if it doesn't already exist with the mass as the key"""
    try:
        cur.execute("""CREATE TABLE `stats` (
        `aircraft_mass` FLOAT NOT NULL,
        `takeoff_distance` FLOAT NOT NULL,
        `takeoff_time` FLOAT NOT NULL,
        `excessive_weight` FLOAT,
        PRIMARY KEY (`aircraft_mass`));""")
    except sqlite3.OperationalError as e: #if it exists already
        pass

def flush_db():
    """Drops the stats table if it doesn't already exist
    """
    try:
        cur.execute("DROP TABLE IF EXISTS `stats`")
    except:
        pass

def save_stats(aircraft_mass, takeoff_distance, takeoff_time, excessive_weight=None):
    """Handles saving the stats of a takeoff, if this mass exists, it won't save anything
    Args:
        aircraft_mass (float): the mass of the plane
        takeoff_distance (float): the takeoff distance
        takeoff_time (float): the takeoff time of the plane
        excessive_weight (None ,float): the excessive weight to save, Defaults to=None
    Returns:
        None 
    """
    try:
        
        cur.execute("""INSERT INTO stats (aircraft_mass, takeoff_distance, takeoff_time, excessive_weight) VALUES (?,?,?,?);""", (aircraft_mass, takeoff_distance, takeoff_time, excessive_weight))
        connection.commit()
    except sqlite3.IntegrityError as e: #if it exists already, no point saving it again
        pass
    except sqlite3.InterfaceError as e: #Another kind of error
        print("Interface error, cannot save takeoff:", e)
