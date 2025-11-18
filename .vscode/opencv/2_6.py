import cv2
import numpy as np

# 读取图像
image = cv2.imread(r"D:\robotstar__visual\2\2\2-6.png")  # 替换为你的图片路径
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 边缘检测
edges = cv2.Canny(gray, 50, 150)

# 查找轮廓
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

image_copy = image.copy()

# 遍历每一个轮廓
for contour in contours:
    # 获取轮廓的多边形拟合
    epsilon = 0.135 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    print(len(approx))
    # 计算轮廓的中心（重心）
    M = cv2.moments(contour)
    if M["m00"] != 0:  # 避免除零错误
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        # 如果轮廓面积为0，使用拟合多边形的第一个点
        cX, cY = approx[0][0]
    
    # 根据拟合的多边形的顶点数判断形状
    if len(approx) == 3:  # 三角形
        colour = (0, 255, 0)
        shape_name = 'Triangle'
    elif len(approx) == 4:  # 四边形
        # 判断正方形还是长方形
        x, y, w, h = cv2.boundingRect(approx)
        aspect_ratio = float(w) / h
        if 0.95 <= aspect_ratio <= 1.05:  # 正方形
            colour = (255, 0, 0)
            shape_name = 'Square'
        else:  # 长方形
            colour = (0, 0, 255)
            shape_name = 'Rectangle'
    
    # 在轮廓中心显示标注文字
    if shape_name:
        cv2.drawContours(image_copy, [approx], -1, colour, 1, cv2.LINE_AA)
        cv2.putText(image_copy, shape_name, (cX, cY),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
        

# 显示结果
cv2.imshow('Detected Shapes', image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
