from time import sleep

from e_drone.drone import *
from e_drone.protocol import *


if __name__ == '__main__':

    drone = Drone()
    drone.open('com3')

    print("TakeOff")
    drone.sendTakeOff()
    sleep(0.01)
        
    print("Hovering")
    drone.sendControlWhile(0, 0, 0, 0, 4000)

    print("Go Start")
    drone.sendControlWhile( 0, 50, 0, 0, 1000)
    drone.sendControlWhile(0, 0, 0, 0, 1000)
    drone.sendControlWhile( 50, 0, 0, 0, 1000)
    drone.sendControlWhile(0, 0, 0, 0, 1000)      
    drone.sendControlWhile( 0, -50, 0, 0, 1000)
    drone.sendControlWhile(0, 0, 0, 0, 1000)
    drone.sendControlWhile( -50, 0, 0, 0, 1000)  
    drone.sendControlWhile(0, 0, 0, 0, 1000)  
    print("Go Stop")
    
    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

    drone.close()
