import cv2 as cv

img = cv.imread('C:\img\codrone.jpg')
print(img.shape)
cv.imshow('window_title',img)

