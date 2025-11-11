import cv2

img = cv2.imread('E:\vscode\opencv\robotstar2025-10-05 001320.jpg')

if img is not None:
    cv2.imshow('Relative Path Example', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("图片读取成功！")