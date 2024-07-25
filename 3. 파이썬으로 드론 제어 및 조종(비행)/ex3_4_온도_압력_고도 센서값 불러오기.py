from time import sleep

from e_drone.drone import *
from e_drone.protocol import *


def eventAltitude(altitude):
    print("eventAltitude()")
    print("-  Temperature: {0:.3f}".format(altitude.temperature))
    print("-     Pressure: {0:.3f}".format(altitude.pressure))
    print("-     Altitude: {0:.3f}".format(altitude.altitude))
    print("- Range Height: {0:.3f}".format(altitude.rangeHeight))


if __name__ == '__main__':

    drone = Drone()
    drone.open('com3')
    
    # 이벤트 핸들링 함수 등록
    drone.setEventHandler(DataType.Altitude, eventAltitude)
    
    while True:

        # Altitude 정보 요청
        drone.sendRequest(DeviceType.Drone, DataType.Altitude)
        sleep(1)

    drone.close()
