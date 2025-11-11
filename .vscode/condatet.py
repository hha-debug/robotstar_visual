import cv2

img = cv2.imread(r'E:\vscode\opencv\robotstar2025-10-05 001320.jpg')

if img is not None:
    cv2.imshow('My Photo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
   