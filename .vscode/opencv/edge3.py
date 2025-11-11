import cv2
import numpy as np
from matplotlib import pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示问题

# 读取图像
image = cv2.imread(r"D:\robotstar__visual\2\2\2-4(1).jpg")
if image is None:
    raise ValueError("图像路径错误或未找到文件")

#  转为灰度并去噪 
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 9, 75, 75)  # 保边去噪(去除亮度变化)

# 边缘检测（Canny）
edges = cv2.Canny(gray, 20, 40)  # 可根据效果微调阈值

# 检测轮廓
contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 绘制轮廓
image_copy = image.copy()
cv2.drawContours(image_copy, contours, -1, (0, 255, 0), 1, cv2.LINE_AA)

plt.figure(figsize=(10, 8), dpi=100)

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(image_copy, cv2.COLOR_BGR2RGB))  # 转为RGB再显示
plt.title('轮廓检测')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray', origin='upper')  # 保持方向一致
plt.title('边缘检测')
plt.axis('off')

plt.tight_layout()
plt.show()