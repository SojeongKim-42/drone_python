import cv2 as cv

img = cv.imread(r'C:\img\drones.jpg',0)  # 여러사진이 있는 사진을 흑백으로 불러옵니다.
a = cv.imread(r'C:\img\codrone.jpg',0)
b = cv.imread(r'C:\img\drones.jpg') #컬러

result = cv.matchTemplate(img, a, cv.TM_SQDIFF)	# 원하는 이미지를 특정화
minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)   # 원하는 이미지의 위치 설정
x, y = minLoc
h,w = a.shape
b = cv.rectangle(b, (x, y), (x + w, y + h), (0,0,255), 2)    # 원하는 이미지에 사각형 표시

cv.imshow("result",b)
cv.waitKey(0)
cv.destroyAllWindows()
