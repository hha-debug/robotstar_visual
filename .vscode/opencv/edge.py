import cv2
import numpy as np

# read the image
image = cv2.imread(r"D:\robotstar__visual\2\2\2-4(1).jpg")
# 灰度图
img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#  均值滤波
blur = cv2.blur(img_gray,(5,5))
#  高斯滤波
blur_gaussian = cv2.GaussianBlur(img_gray,(3,3),1)
# 查找轮廓
ret, thresh = cv2.threshold(blur_gaussian , 150, 255, cv2.THRESH_BINARY)
# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE)
                                     
# draw contours on the original image
image_copy = image.copy()
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 1, cv2.LINE_AA)
               
# see the results
cv2.imshow('None approximation', image_copy)
cv2.waitKey(0)
cv2.imwrite('contours_none_image1.jpg', image_copy)
cv2.destroyAllWindows()
