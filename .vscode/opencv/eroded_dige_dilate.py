import cv2
import os
import numpy as np



# 读取图像
img = cv2.imread(r"D:\robotstar__visual\2\2\2-2.png")
if img is None:
    print("图片读取失败，请检查路径是否正确")
else:
    
    # 创建结构元素
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3)) 
    cv2.imshow("img_row",img)
    cv2.waitKey(0)
    
    eroded = cv2.erode(img, kernel, iterations = 1)
    cv2.imshow(f"erode_img", eroded)
    cv2.waitKey(0)
    kernel = np.ones((3,3),np.uint8) 
    dige_dilate = cv2.dilate(eroded,kernel,iterations = 1)

    cv2.imshow('dilate', dige_dilate)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


