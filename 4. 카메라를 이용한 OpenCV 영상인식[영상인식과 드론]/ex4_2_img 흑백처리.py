import cv2 as cv

img = cv.imread('C:\img\codrone.jpg')
print(img.shape)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('window_title',img_gray)

