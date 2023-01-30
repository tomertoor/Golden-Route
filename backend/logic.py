
SHIMSHON_ENGINE_FORCE = 100000 # in nuetons
SHIMSHON_TAKEOFF_VELOCITY = 140 # in m per second

MAX_TAKEOFF_TIME = 60

TAKEOFF_DISTANCE_CELL = 0
TAKEOFF_TIME_CELL = 1
OVERWEIGHT_MASS_CELL = 2

def calculate_acceleration(force, mass):
    """Calculates acceleration by force and mass

    Args:
        force (int): the force of the engine
        mass (int): the mass of the plane

    Returns:
        float: the acceleration. 
    """
    return force / mass
    
def calculate_velocity(acceleration, time):
    """Calculates velocity by acceleration and time
    Args:
        acceleration (int): the acceleration of the plane
        time (int): the time in seconds

    Returns:
        float: the velocity of the plane 
    """
    return acceleration * time

def calculate_takeoff_time(acceleration, velocity):
    """Calculates the time in which the plane will reach a velocity in a given acceleration
    Args:
        acceleration (int): the acceleration of the plane
        velocity (int): the velocity it needs to reach

    Returns:
        float: the time it will take for the plane to takeoff 
    """
    return velocity / acceleration


def calculate_takeoff_distance(acceleration, time, start_pos=0, start_velocity=0):
    """Calculates the takeoff distance of a given plane, based on acceleration, time, velocity at the beginning of takeoff and the starting position
    Args:
        acceleration (int): the acceleration of the plane
        time (int): the it will take for the plane to takeoff
    Returns: float: the takeoff distance
    """
    return (0.5 * acceleration *  pow(time, 2)) + (start_velocity * time) + start_pos

def calculate_takeoff_stats(mass):
    acceleration = calculate_acceleration(SHIMSHON_ENGINE_FORCE, mass)
    time = calculate_takeoff_time(acceleration, SHIMSHON_TAKEOFF_VELOCITY)
    takeoff_distance = calculate_takeoff_distance(acceleration, time)

    result = [takeoff_distance, time] #here so it the overweight wont change the result and will just display the overweight

    overweight_mass = 0
    
    
    while time > MAX_TAKEOFF_TIME:
        mass -= 1
        overweight_mass += 1
        acceleration = calculate_acceleration(SHIMSHON_ENGINE_FORCE, mass)
        time = calculate_takeoff_time(acceleration, SHIMSHON_TAKEOFF_VELOCITY)
    
    result.append(overweight_mass) if overweight_mass > 0 else None
    
    return result