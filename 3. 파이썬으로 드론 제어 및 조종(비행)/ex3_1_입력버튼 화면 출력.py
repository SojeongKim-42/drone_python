from time import sleep

from e_drone.drone import *
from e_drone.protocol import *

1+2


def eventButton(button):
    print(button.button)    

if __name__ == '__main__':
    drone = Drone()
    drone.open('com3')

    # 이벤트 핸들링 함수 등록
    drone.setEventHandler(DataType.Button, eventButton)

    drone.sendPing(DeviceType.Controller)

    for i in range(100, 0, -1):
        print(i)
        sleep(1)

    drone.close()
