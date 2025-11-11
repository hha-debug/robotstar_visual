import cv2
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 读取图像
image = cv2.imread(r"D:\robotstar__visual\2\2\2-5.jpg")
if image is None:
    raise ValueError("图像路径错误或未找到文件")

#  转为灰度并去噪 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)  # 保边去噪(去除亮度变化)

# 边缘检测（Canny）
edges = cv2.Canny(gray, 20, 40)  # 可根据效果微调阈值

# 检测轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 遍历所有轮廓，计算每个轮廓的面积，周长
if contours:  # 确保有轮廓被检测到
    for i, cnt in enumerate(contours):
        area = cv2.contourArea(cnt, oriented=False)  # 传入单个轮廓
        length = cv2.arcLength(cnt,closed=True) 
        print(f"轮廓 {i+1} 的面积是：{area:.2f} 像素")
        print(f"轮廓 {i+1} 的周长是：{length:.2f} 像素")
else:
    print("未检测到任何轮廓")

# 显示结果
cv2.imshow("Bounding Rectangles", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
image_copy = image.copy()
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 1, cv2.LINE_AA)

# 遍历轮廓，计算并绘制外接矩形
for cnt in contours:
    # 计算最小外接矩形
    x, y, w, h = cv2.boundingRect(cnt)
    
    # 在图像上绘制矩形（绿色，线宽2）
    cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # 打印矩形信息
    print(f"矩形：左上角({x}, {y})，宽{w}，高{h}，面积{w*h}")
               
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 1, cv2.LINE_AA)
               
cv2.imshow('boundingRect', image_copy)
cv2.waitKey(0)
cv2.imwrite('contours_none_image1.jpg', image_copy)
cv2.destroyAllWindows()
