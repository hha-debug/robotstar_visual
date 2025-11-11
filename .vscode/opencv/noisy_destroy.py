import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题
# 1 图像读取
img = cv.imread(r"D:\robotstar__visual\2\2\2-3.jpg")
# 2 均值滤波
blur = cv.blur(img,(5,5))
# 3 高斯滤波
blur_gaussian = cv.GaussianBlur(img,(3,3),1)
# 3 图像显示
plt.figure(figsize=(10,8),dpi=100)
plt.subplot(131),plt.imshow(img[:,:,::-1]),plt.title('原图')
plt.xticks([]), plt.yticks([])
plt.subplot(132),plt.imshow(blur[:,:,::-1]),plt.title('均值滤波后结果')
plt.xticks([]), plt.yticks([])
plt.subplot(133),plt.imshow(blur_gaussian[:,:,::-1]),plt.title('高斯滤波后结果')
plt.xticks([]), plt.yticks([])
plt.show()