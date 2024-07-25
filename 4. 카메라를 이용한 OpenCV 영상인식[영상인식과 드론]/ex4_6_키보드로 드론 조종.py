from time import sleep
from e_drone.drone import *
from e_drone.protocol import *
import keyboard

drone = Drone()
drone.open("com3")

while True:
    if keyboard.is_pressed("1"):
        print("TakeOff")
        sleep(2)
        drone.sendTakeOff()        
        drone.sendControlWhile(0, 0, 0, 0, 2000) 
    elif keyboard.is_pressed("0"):
        print("Landing")
        drone.sendLanding()
        sleep(0.01)
        drone.sendLanding()
        sleep(0.01)
    elif keyboard.is_pressed("w"):
        print("Up")
        drone.sendControl(0, 0, 0, 50)
    elif keyboard.is_pressed("s"):
        print("Down")
        drone.sendControl(0, 0, 0, -50)
    elif keyboard.is_pressed("a"):
        print("CCW")
        drone.sendControl(0, 0, 50, 0)
    elif keyboard.is_pressed("d"):
        print("CW")
        drone.sendControl(0, 0, -50, 0)
    elif keyboard.is_pressed("up"):
        print("Forward")
        drone.sendControl(0, 50, 0, 0)
    elif keyboard.is_pressed("down"):
        print("Back")
        drone.sendControl(0, -50, 0, 0)
    elif keyboard.is_pressed("left"):
        print("Left")
        drone.sendControl(-50, 0, 0, 0)
    elif keyboard.is_pressed("right"):
        print("Right")
        drone.sendControl(50, 0, 0, 0)
