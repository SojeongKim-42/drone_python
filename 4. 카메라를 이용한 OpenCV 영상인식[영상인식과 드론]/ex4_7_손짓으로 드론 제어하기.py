from e_drone.drone import *
from e_drone.protocol import *

import cv2
import keyboard

from time import sleep

##############################################################################################################

face_detector = cv2.CascadeClassifier()
#face_detector.load(r'C:\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')
face_detector.load(r'C:\Users\gs00\AppData\Local\Programs\Python\Python312\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')

def face(image, window, ROI, W, H):
    roi = image[H - ROI :H + ROI, W - ROI:W + ROI]
    faces = face_detector.detectMultiScale(roi, 1.3, 5, 10)

    if(len(faces) == 0): return False
    else: return True
        
##############################################################################################################

point_color = (0,0,255)
font_big = 0.5
simple_color = (255,255,255)
font_small = 0.5

def putTextonFrame(frame, differ_ = 0, sum_ = 0, THRE_DIFFER = 0, THRE_SUM = 0):
    font = cv2.FONT_HERSHEY_DUPLEX
    h,w,_ = frame.shape
    w = int(w/15)
    cv2.rectangle(frame, (0,0), (150, 2 * w + 20), (0,0,0), -1)
    
    differ_ = abs(differ_)
    if(THRE_SUM < sum_ and THRE_DIFFER < differ_):
        color_ = point_color
        font_size = font_big
    else:
        color_ = simple_color
        font_size = font_small

    if(THRE_DIFFER < 1): THRE_DIFFER = 1
    cv2.putText(frame, "DIFFER : "  + "{:3d}".format(int(differ_/THRE_DIFFER * 100),2) + "%", (0, 1*w), font, font_size, color_, 1, cv2.LINE_AA)

    if(THRE_SUM < sum_):
        color_ = point_color
        font_size = font_big
    else:
        color_ = simple_color
        font_size = font_small

    cv2.putText(frame, "POWER : " + "{:3d}".format(int(sum_/THRE_SUM * 100)) + "%", (0, 2*w), font , font_size, color_, 1, cv2.LINE_AA)

##############################################################################################################

class FlappyBird:
    def __init__(self):
        # --------------------#
        # PARAMETER
        self.ROI = 100
        self.resize_num = 0.3
        self.DIFFER_PERCENT = 0.7
        self.MOVE = 3000
        
        # drone motor
        self.PITCH = 0
        self.ROLL = 30
        self.THRO_UP = 80
        self.THRO_DOWN = -30
        self.LOW_THRO_UP = 20
        # ---------------------#

        #self.drone = Drone()
        self.cap = cv2.VideoCapture(0)
        self.frame_name = "frame"

        self.quit = 0
				
        self.now_roll = 0
        self.now_pitch = 0
        self.now_yaw = 0
        self.now_throttle = 0

        # Continuous command time

        self.frame_cnt = 0
        self.right_area = 0
        self.left_area = 0

        
##############################################################################################################

    def face_detect(self, frame):
        h, w, _ = frame.shape
        w_half = int(w / 2)	# 320
        h_half = int(h / 2)	# 240
        h_quar = int(h / 4)	# 120
        font = cv2.FONT_HERSHEY_DUPLEX
        
        if (h_quar < self.ROI or w_half < self.ROI): print("ROI IS TOO BIG!")
        
        while (not face(frame, self.frame_name, self.ROI, w_half, h_quar)):        	
            cv2.rectangle(frame, (w_half - self.ROI, h_quar - self.ROI), (w_half + self.ROI, h_quar + self.ROI), (100, 100, 200), 8)           
            cv2.imshow(self.frame_name, frame)
            cv2.waitKey(1)
            ret, frame = self.cap.read()
            frame = cv2.flip(frame, 1)
                            
        # Show the starting image
        cv2.rectangle(frame, (int(w_half - w_half/2), int(h_half - w_half/2)), (int(w_half + w_half/2), int(h_half + w_half/2)), (150, 150, 150), 10)                
        cv2.putText(frame, "START ", (w_half - 135, h_half + 20) , font , 3, (255, 255, 255), 3)
                    
        cv2.imshow(self.frame_name, frame)
        cv2.waitKey(1)

##############################################################################################################

    def divide_screen(self, frame, pre_frame):

        frame = cv2.resize(frame, None, fx=self.resize_num, fy=self.resize_num)
        now_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.absdiff(pre_frame, now_frame)
        frame = cv2.threshold(frame, 40, 255, cv2.THRESH_BINARY)[1]
        h, w = frame.shape
        right_frame = frame[:, int(w * 0.55):]
        left_frame = frame[:, 0:int(w * 0.45)]
        right_num = cv2.countNonZero(right_frame)
        left_num = cv2.countNonZero(left_frame)
        ee1 = cv2.getTickCount()

        return now_frame, right_num, left_num
        
##############################################################################################################
  
    def draw_for_debug(self, frame, sum, differ):
    	
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape

        # right
        if (self.now_roll < 0):
            #cv2.rectangle(frame, (w - 10, 0), (w-1, h), (200, 200, 200), 5)
            cv2.circle(frame, (int(w/2 - 240) , int(h/2)), 60, (200, 100, 100), 5)
        # left
        elif (self.now_roll > 0):
            #cv2.rectangle(frame, (1, 0), (10, h), (200, 200, 200), 5)
            cv2.circle(frame, (int(w/2 + 240) , int(h/2)), 60, (200, 100, 100), 5)
        # up
        elif (self.now_throttle > self.LOW_THRO_UP):        	
            #cv2.rectangle(frame, (0, 1), (w, 10), (200, 200, 200), 5)
            cv2.circle(frame, (int(w/2 - 240) , int(h/2)), 60, (200, 100, 100), 5)
            cv2.circle(frame, (int(w/2 + 240) , int(h/2)), 60, (200, 100, 100), 5)            
        # down
        elif (self.now_throttle == self.THRO_DOWN):
            #cv2.rectangle(frame, (0, w - 10), (w-1, h), (200, 200, 200), 5)
            cv2.circle(frame, (int(w/2) , int(h/2 + 160)), 60, (200, 100, 100), 5)  
            
        putTextonFrame(frame=frame, differ_=differ, sum_=sum,
                       THRE_DIFFER=self.DIFFER_PERCENT * sum,
                       THRE_SUM=self.MOVE)
        return frame

##############################################################################################################
          
    def run(self, port_name=None, drone_name=None):   
    	    
        # face detection use
        face_detection = 1
        
        while (self.quit == 0):
            e1 = cv2.getTickCount()
            
            ### Port open
            drone = Drone('com3')
            drone.open()
				
            ### vedio capture and save to previous frame
            if (self.cap.isOpened()):
                ret, frame = self.cap.read()
                frame = cv2.flip(frame, 1)
                pre_frame = cv2.resize(frame, None, fx=self.resize_num, fy=self.resize_num)
                pre_frame = cv2.cvtColor(pre_frame, cv2.COLOR_BGR2GRAY)
            else:
                print("video is not opened!")

            cv2.namedWindow(self.frame_name, cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty(self.frame_name, cv2.WND_PROP_VISIBLE, cv2.WINDOW_FULLSCREEN)
            cv2.imshow(self.frame_name, frame)
            cv2.waitKey(1)
                        
            ### Start with face detection
            print("Start with face detection!")
            if (face_detection == 1):
                self.face_detect(frame)

            ### Start with takeoff           
                        
            drone.sendTakeOff()
            sleep(0.1)
            drone.sendTakeOff()
            sleep(0.1)
            drone.sendTakeOff()
            sleep(0.1)            
            drone.sendControlWhile(0, 0, 0, 0, 4000)            
            
            print("Control!!")
            
            while (self.cap.isOpened() and self.quit is 0):
                ret, frame = self.cap.read()
                self.frame_cnt += 1
                pre_frame, r, l = self.divide_screen(frame, pre_frame)
                self.right_area += r
                self.left_area += l

                ### Send the commands every 5 frame
                if (self.frame_cnt == 4):
                    sum = self.right_area + self.left_area
                    differ = self.left_area - self.right_area
                    
                    #initial frame cnt
                    self.frame_cnt, self.right_area, self.left_area = 0, 0, 0
                    
                    #print("Find face!!")                                         
                    roll_flag = 1
                    DIFFER_THRESH = self.DIFFER_PERCENT * sum
                    
                    # right
                    # go left
                    if (roll_flag and differ > DIFFER_THRESH and sum > self.MOVE / 2):
                    	print("right")    
                    	#drone.sendControl(self.ROLL, 0, 0, self.LOW_THRO_UP)                    	
                    	self.now_roll = self.ROLL
                    	self.now_pitch = 0
                    	self.now_yaw = 0
                    	self.now_throttle = self.LOW_THRO_UP         	
                    	
                    # left
                    # go right
                    elif (roll_flag and differ < -DIFFER_THRESH and sum > self.MOVE / 2):
                    	print("left")
                    	#drone.sendControl(-self.ROLL, 0, 0, self.LOW_THRO_UP)                    	
                    	self.now_roll = -self.ROLL
                    	self.now_pitch = 0
                    	self.now_yaw = 0
                    	self.now_throttle = self.LOW_THRO_UP         	
                    	      
                    # up
                    elif (sum > self.MOVE):
                    	print("up")
                    	#drone.sendControl(0, self.PITCH, 0, self.THRO_UP)                    	
                    	self.now_roll = 0
                    	self.now_pitch = self.PITCH
                    	self.now_yaw = 0
                    	self.now_throttle = self.THRO_UP  
                    	
                    # down                    
                    else:
                    	print("down")
                    	#drone.sendControl(0, 0, 0, self.THRO_DOWN)                    	
                    	self.now_roll = 0
                    	self.now_pitch = 0
                    	self.now_yaw = 0
                    	self.now_throttle = self.THRO_DOWN                    	
                                        
                    drone.sendControl(self.now_roll, self.now_pitch, self.now_yaw, self.now_throttle)
                    print(self.now_roll, self.now_pitch, self.now_yaw, self.now_throttle)               
                    # time stuff-----------------------------------------------------------------------
                    e2 = cv2.getTickCount()
                    timePassed = (e2 - e1) / cv2.getTickFrequency()
                    e1 = e2
                    fps = 1 / timePassed
                    print("fps : ", format(fps,".2f"))
                    
                    frame = self.draw_for_debug(frame, sum, differ)
                    
                    cv2.imshow(self.frame_name, frame)
                    cv2.waitKey(1)
   
                if cv2.waitKey(1) & 0xFF == ord("q"):				
                    drone.sendStop()				
                    self.quit = 1
                    break

                if keyboard.is_pressed("1"):
                    print("TakeOff") 
                    drone.sendTakeOff()
                    sleep(0.01)
                    drone.sendControlWhile(0, 0, 0, 0, 4000)       
                elif keyboard.is_pressed("0"):
                    print("Landing")
                    drone.sendLanding()
                    sleep(0.01)
                elif keyboard.is_pressed("W"):
                    print("Up")
                    drone.sendControl(0, 0, 0, 50)
                elif keyboard.is_pressed("S"):
                    print("Down")
                    drone.sendControl(0, 0, 0, -50)
                elif keyboard.is_pressed("Up"):
                    print("Forward")
                    drone.sendControl(0, 50, 0, 0)
                elif keyboard.is_pressed("Down"):
                    print("Backward")
                    drone.sendControl(0, -50, 0, 0)
                elif keyboard.is_pressed("Left"):
                    print("Left")
                    drone.sendControl(-50, 0, 0, 0)
                elif keyboard.is_pressed("Right"):
                    print("Right")
                    drone.sendControl(50, 0, 0, 0)
                elif keyboard.is_pressed("Space"):
                    print("Space")
                    drone.sendControl(0, 0, 0, 0)        
                
        self.cap.release()
        drone.close()

if __name__ == "__main__":
    FlappyBird().run()
