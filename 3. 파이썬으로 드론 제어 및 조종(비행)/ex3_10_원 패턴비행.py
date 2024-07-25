from time import sleep

from e_drone.drone import *
from e_drone.protocol import *


if __name__ == '__main__':

    drone = Drone()
    drone.open()

    print("TakeOff")
    drone.sendTakeOff()
    sleep(0.01)
        
    print("Hovering")
    drone.sendControlWhile(0, 0, 0, 0, 4000)

    print("Go Start")
    drone.sendControlWhile( 50, 0, -60, 25, 5000)

        
    print("Go Stop")
    drone.sendControlWhile(0, 0, 0, 0, 1000)
    
    
    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

    drone.close()
