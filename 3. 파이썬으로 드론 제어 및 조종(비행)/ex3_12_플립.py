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

    print("Flip")
    drone.sendFlightEvent(FlightEvent.FlipFront)
    sleep(1)
    
    print("Hovering")
    drone.sendControlWhile(0, 0, 0, 0, 3000)
    
    print("Landing")
    drone.sendLanding()
    sleep(0.01)
    drone.sendLanding()
    sleep(0.01)

    drone.close()
