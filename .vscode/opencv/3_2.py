import cv2
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False   

# 读取图像
image = cv2.imread(r"D:\robotstar__visual\2\2\3-1-2.jpg")
if image is None:
    raise ValueError("图像路径错误或未找到文件")

#  转为灰度并去噪 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)  # 保边去噪(去除亮度变化)
kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) 
    
eroded = cv2.erode(gray, kernel, iterations = 10)
kernel = np.ones((3,3),np.uint8) 
dige_dilate = cv2.dilate(eroded,kernel,iterations = 20)
cv2.imshow("dige_dilate",dige_dilate)
# 边缘检测（Canny）
edges = cv2.Canny(dige_dilate, 50, 150)  
cv2.imshow("edges",edges)
# 检测轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
image_copy = image.copy()

# 挑选轮廓
contours_1 = []
if contours:
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt, oriented=False)  # 传入单个轮廓
        if area == 10.0 or area == 30.50:
            contours_1.append(cnt)
            print(f"轮廓 {i+1} 的面积是：{area:.2f} 像素")
        
               
cv2.drawContours(image_copy, contours_1, -1, (0, 0, 255), 1, cv2.LINE_AA)
               
cv2.imshow('boundingRect', image_copy)
cv2.waitKey(0)
cv2.imwrite('contours_none_image1.jpg', image_copy)
cv2.destroyAllWindows()
