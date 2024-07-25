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
    drone.sendControlWhile(0, 0, 0, 0, 5000)
    
    print("ZIGZAG")
    for i in range(4,0,-1):
        drone.sendControlWhile(0, 0, -30, 0, 800)
        drone.sendControlWhile(0, 30, 0, 0, 1000)
        drone.sendControlWhile(0, 0, 30, 0, 800)
        drone.sendControlWhile(0, 30, 0, 0, 1000)
        
    print("Hovering")
    drone.sendControlWhile(0, 0, 0, 0, 2000)
    
    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

    drone.close()
