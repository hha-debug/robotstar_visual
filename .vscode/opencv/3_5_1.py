import time
import collections
import cv2
import numpy as np
from loguru import logger 

PRINTS_PER_SECOND = 1  # 每秒打印一次
PRINT_FRAME_INTERVAL = 1  # 默认间隔

def detect_and_annotate(frame):
    """检测黄色和绿色目标并标注"""
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # 转到HSV颜色空间 H 色相 S 饱和度 V 亮度

    detections = [] # 用于保存检测到的目标信息 每项为 (id, cx, cy, box)

    # 黄色检测
    lower_yellow = np.array([20, 150, 150])
    upper_yellow = np.array([35, 255, 255]) # 只保留色相在20—35之间的黄色，饱和度和亮度较高排除衣服颜色干扰
    mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow) # 二值掩膜
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)) # 创建一个 5×5 的椭圆形结构元素，常用于形态学操作的核。
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_OPEN, kernel) # 开运算
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, kernel) # 闭运算

    contours_y, _ = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_y:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        rect = cv2.minAreaRect(cnt) # 计算最小外接旋转矩形，返回 center ((x,y), (width, height), angle)
        box = cv2.boxPoints(rect).astype(int) # 获取四个顶点坐标
        cx, cy = int(rect[0][0]), int(rect[0][1]) 
        detections.append((0, cx, cy, box))

    # 绿色检测
    lower_green = np.array([40, 60, 60])
    upper_green = np.array([90, 255, 255])
    mask_g = cv2.inRange(hsv, lower_green, upper_green)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_OPEN, kernel)
    mask_g = cv2.morphologyEx(mask_g, cv2.MORPH_CLOSE, kernel)

    contours_g, _ = cv2.findContours(mask_g, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_g:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect).astype(int)
        cx, cy = int(rect[0][0]), int(rect[0][1])
        detections.append((1, cx, cy, box))

    # 绘制结果
    for det in detections:
        id_, cx, cy, box = det
        color = (0, 255, 255) if id_ == 0 else (0, 255, 0)
        cv2.drawContours(vis, [box], 0, color, 2)
        text = f"ID:{id_} ({cx},{cy})"
        cv2.putText(vis, text, (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2) # 在指定位置 (cx - 40, cy - 10) 绘制一段文字 text
        cv2.circle(vis, (cx, cy), 3, (255, 0, 0), -1) # 画中心圆

    return vis, detections


def main():
    src = r"D:\robotstar__visual\2\2\3-2.mp4"

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        logger.error("Failed to open capture source")
        return

    fps_hist = collections.deque(maxlen=30) # 用于存储最近最多 30 个帧处理时间对应的瞬时 FPS（用来平滑显示平均 FPS）
    frame_count = 0

    fps_input = cap.get(cv2.CAP_PROP_FPS) # 尝试读取视频文件内置的帧率信息
    if fps_input <= 0:
        fps_input = 30
    delay = int(1000 / fps_input) # 等待时间，按原视频速度播放

    last_print_time = time.time()

    try:
        while True:
            ret, frame = cap.read() # 读取下一帧；ret 为 False 表示到视频末尾或读取失败
            if not ret:
                break

            t0 = time.time()
            vis, detections = detect_and_annotate(frame)
            t1 = time.time()
            fps = 1.0 / (t1 - t0) if (t1 - t0) > 0 else 0
            fps_hist.append(fps)
            avg_fps = sum(fps_hist) / len(fps_hist)

            cv2.putText(vis, f"FPS: {avg_fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2) # 在图像左上角绘制平均 FPS

            frame_count += 1
            now = time.time()

            if now - last_print_time >= 1.0 / PRINTS_PER_SECOND:
                for det in detections:
                    id_, cx, cy, _ = det
                    logger.info(f"检测到目标 ID:{id_} 坐标=({cx},{cy})")
                last_print_time = now

            cv2.imshow('Detection', vis)
            key = cv2.waitKey(delay) & 0xFF
            if key == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
