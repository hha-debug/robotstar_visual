import cv2


cv2.namedWindow('img',cv2.WINDOW_NORMAL)
img = cv2.imread(r"E:\vscode\opencv\robotstar2025-10-05 001320.jpg")
while True:
    cv2.imshow('img',img)
    key = cv2.waitKey(0)
    #print(key)
    #print('q')
    #print(ord('q'))

    if (key & 0Xff == ord('q')):
        print("123")
        break
    elif(key == ord('s')):
        cv2.imwrite(r"E:\vscode\opencv\123.png",img)
    else:
        print(key)
cv2.destroyAllWindows()