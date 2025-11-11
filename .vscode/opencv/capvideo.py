import cv2

fourcc = cv2.VideoWriter_fourcc(*'MJPG')
vw = cv2.VideoWriter('./out.mp4',fourcc,25,(1920,1080))
#创建窗口
cv2.namedWindow('video',cv2.WINDOW_NORMAL)

#获取视频设备/读取视频文件 读取视频帧
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read(1)


    cv2.imshow('video',frame)
    #写数据到媒体文件
    vw.write(frame)
    key = cv2.waitKey(40)
    if(key & 0xff == ord('q')):
        break

#释放capture
cv2.release()
vw.release()
cv2.destroyAllWindows()

