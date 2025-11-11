import cv2
import os
img=cv2.imread(r"D:\robotstar__visual\2\2\2-4(1).jpg")
#生成灰度图，注意此步骤
gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

def cv_show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
#生成二值图像，方便查找轮廓
ret,img_black=cv2.threshold(gray,100,200,cv2.THRESH_BINARY)
#轮廓查找，查找有层级的全部轮廓
contours,hierarchy=cv2.findContours(img_black,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
#复制原始彩色图，不复制的话，在绘制轮廓时会对原始图像进行修改
draw_img=img.copy()
#在彩色图像上绘制轮廓
#注意：只有在彩色图像上才能画出彩色轮廓，如为灰度图，无论drawContours中关于颜色的信息如何设置，都只能生成黑色轮廓
res=cv2.drawContours(draw_img,contours,-1,(0 ,0,255),1)
cv_show('res',res)