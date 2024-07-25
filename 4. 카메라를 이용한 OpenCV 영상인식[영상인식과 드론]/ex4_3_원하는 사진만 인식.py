import cv2 as cv

img = cv.imread(r'C:\img\drones.jpg',0)
a = cv.imread(r'C:\img\codrone.jpg',0)
b = cv.imread(r'C:\img\drones.jpg') #컬러

result = cv.matchTemplate(img, a, cv.TM_SQDIFF)	
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)
x, y = minLoc
h,w = a.shape
b = cv.rectangle(b, (x, y), (x + w, y + h), (0,0,255), 2)

cv.imshow("result",b)
cv.waitKey(0)
cv.destroyAllWindows()
