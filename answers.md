
# Part 1 Questions:

## Question 5

Edge cases that can pop when using the system is when the mess of the aircraft is 0, it would cause a division by zero and throw an exception.

## Question 6
To make the physical formula more accurate it should take into account:
- Outside air temperature
- The altimeter (field pressure, usually in qnh or bars)
- Wind component (usually planes takeoff against the wind to create lift so it needs to be considered)
-  Obstacle height
- Dew point 
# Part 4 Questions:

## Question 4
The other details that should be shown is:
- Sea-level pressure
- Wind direction and speed at 10m (used to choose to active runway and what to expect when asking for clearence from ATC)
- Wind gusts 
- Visibility (to determine whether flight rules should be IFR or CVFR)
- Dewpoint
- Temperature

# Part 7 Questions:

## Question 1:
The risks for operational system is first of all the reliabality on the internet, when an endpoint is exposed to the internet, it can be exploited in one way or another. Another risk is dependencies and deprecation, sometimes a dependency of a system can have an update which features that the system uses will be depracated or won't work as expected and therefore the system won't work.

## Question 2:
To minimize the risk it is recommended to try and put the system under a closed network with no access to the outside internet. If it has to use an external source then I would recommend using a proxy so the connection won't be exposed. For the second risk I think that you need to have maintainance team that will check the program every time there is an update (can be QA aswell).