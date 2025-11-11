import  cv2
from loguru import logger

# 配置loguru：输出到控制台和文件，设置日志格式和级别
logger.add(
    "circle_detection.log",  # 日志文件路径
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 日志格式
    level="INFO",  # 日志级别（INFO及以上会被记录）
    rotation="1 MB"  # 日志文件超过1MB自动分割
)
try:
    #载入并显示图片
    img=cv2.imread(r"D:\robotstar__visual\2\2\3-1-1.jpg")
except Exception as e:
    logger.error(f"载入图片失败：{str(e)}")
    exit()
#灰度化
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#输出图像大小，方便根据图像大小调节minRadius和maxRadius
print(img.shape)

#霍夫变换圆检测
try:
    circles= cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=100,param2=30,minRadius=5,maxRadius=100)
    #输出返回值，方便查看类型
    print(circles)
    #输出检测到圆的个数
    print(len(circles[0]))

    #根据检测到圆的信息，画出每一个圆
    for circle in circles[0]:
        #圆的基本信息
        print(circle[2])
        #坐标行列
        x=int(circle[0])
        y=int(circle[1])
        #半径
        r=int(circle[2])
        #在原图用指定颜色标记出圆的位置
        img=cv2.circle(img,(x,y),r,(30,255,255),-1)
except Exception as e:
    logger.error(f"霍夫圆检测失败：{str(e)}")
    exit()
#显示新图像
cv2.imshow('res',img)

#按任意键退出
cv2.waitKey(0)
cv2.destroyAllWindows()
