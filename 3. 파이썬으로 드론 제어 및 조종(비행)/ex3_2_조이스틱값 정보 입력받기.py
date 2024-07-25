from time import sleep

from e_drone.drone import *
from e_drone.protocol import *


def eventJoystick(joystick):
    print(joystick.left.x, joystick.left.y, joystick.right.x, joystick.right.y)

if __name__ == '__main__':
    drone = Drone()
    drone.open('com3')

    # 이벤트 핸들링 함수 등록
    drone.setEventHandler(DataType.Joystick, eventJoystick)

    drone.sendPing(DeviceType.Controller)

    for i in range(10, 0, -1):
        print(i)
        sleep(10)

    drone.close()
