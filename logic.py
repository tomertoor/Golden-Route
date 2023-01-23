
SHIMSHON_ENGINE_FORCE = 1000000 # in nuetons
SHIMSHON_TAKEOFF_VELOCITY = 140 # in m per second

def calculate_acceleration(force, mass):
    """Calculates acceleration by force and mass

    Args:
        force (int): the force of the engine
        mass (int): the mass of the plane

    Returns:
        float: the acceleration. 
    """
    return force / mass
    
def calculate_velocity(acceleration, time)
    """Calculates velocity by acceleration and time
    Args:
        acceleration (int): the acceleration of the plane
        time (int): the time in seconds

    Returns:
        float: the velocity of the plane 
    """
    return acceleration * time

def calculate_takeoff_time(acceleration, velocity)
    """Calculates the time in which the plane will reach a velocity in a given acceleration
    Args:
        acceleration (int): the acceleration of the plane
        velocity (int): the velocity it needs to reach

    Returns:
        float: the time it will take for the plane to takeoff 
    """
    return velocity / acceleration


def calculate_takeoff_time(acceleration, time, start_pos=0, start_velocity=0)
    
    
    pass

def calculate_takeoff_stats(mass)
    acceleration = calculate_acceleration(SHIMSHON_ENGINE_FORCE, mass)
    time = calculate_takeoff_time(acceleration, SHIMSHON_TAKEOFF_VELOCITY)
    calculate_takeoff_time(acceleration, time)


