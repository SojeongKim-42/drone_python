import random
from time import sleep

from e_drone.drone import *
from e_drone.protocol import *


if __name__ == '__main__':

    drone = Drone(True, True, True, True, True)
    drone.open('com3')

    while True:

        drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 5, 255, 0, 0)
        sleep(2)
        drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 5, 0, 255, 0)
        sleep(2)
        drone.sendLightDefaultColor(LightModeDrone.BodyDimming, 5, 0, 0, 255)
        sleep(2)
        
    drone.close()
