import cv2


#创建窗口
cv2.namedWindow('video',cv2.WINDOW_NORMAL)

#获取视频设备
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read(1)


    cv2.imshow('video',frame)
    key = cv2.waitKey(1)
    if(key & 0xff == ord('q')):
        break

#释放capture
cv2.release()
cv2.destroyAllWindows()