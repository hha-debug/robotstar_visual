import time
import threading
import collections
import queue
import cv2
import numpy as np
from loguru import logger


class FrameGrabber(threading.Thread):
    """持续从视频源中读取图像帧并放入队列，用于在后台持续读取视频帧，避免主线程因 I/O 阻塞"""
    def __init__(self, cap, q, name='FrameGrabber'):
        super().__init__(daemon=True)
        self.cap = cap
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                self.running = False
                break
            try:
                if self.q.full():
                    _ = self.q.get_nowait() # 如果队列满了（表示主线程处理慢），弹出（丢弃）最旧的帧，保持队列只保存最近帧，避免内存持续增长并保持“最新优先”
                self.q.put_nowait(frame)
            except Exception:
                pass

    def stop(self):
        self.running = False


def detect_and_annotate(frame):
    """检测黄色与绿色目标并绘制标注

    返回：
        vis: 标注后的图像
        detections: 检测结果列表 [(id, cx, cy, box_points), ...]
    """
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detections = []

    lower_yellow = np.array([20, 150, 150])
    upper_yellow = np.array([35, 255, 255])
    mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_OPEN, kernel)
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, kernel)

    contours_y, _ = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_y:
        area = cv2.contourArea(cnt)
        if area < 200:
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect).astype(int)
        cx, cy = int(rect[0][0]), int(rect[0][1])
        detections.append((0, cx, cy, box))

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

    for det in detections:
        id_, cx, cy, box = det
        color = (0, 255, 255) if id_ == 0 else (0, 255, 0)
        cv2.drawContours(vis, [box], 0, color, 2)
        text = f"ID:{id_} ({cx},{cy})"
        cv2.putText(vis, text, (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.circle(vis, (cx, cy), 3, (255, 0, 0), -1)

    return vis, detections


def main():
    src = r"D:\robotstar__visual\2\2\3-2.mp4"

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        logger.error("无法打开视频源")
        return

    frame_q = queue.Queue(maxsize=2) # 用于存储视频帧的队列，最大容量为2帧
    grabber = FrameGrabber(cap, frame_q) # 创建实例 分配线程ID
    grabber.start() # 启动线程

    fps_hist = collections.deque(maxlen=30)

    logger.info("开始目标检测... 按下 'q' 键可退出程序")

    try:
        while True:
            try:
                frame = frame_q.get(timeout=1.0) # 获取最新帧
            except queue.Empty:
                if not grabber.is_alive():
                    logger.warning("视频源结束或采集线程已停止")
                    break
                continue

            t0 = time.time()
            vis, detections = detect_and_annotate(frame)
            t1 = time.time()

            fps_hist.append(1.0 / (t1 - t0) if (t1 - t0) > 0 else 0)
            fps = sum(fps_hist) / len(fps_hist) if fps_hist else 0.0

            cv2.putText(vis, f"FPS: {fps:.1f}", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            for det in detections:
                id_, cx, cy, _ = det
                logger.info(f"检测到目标：ID={id_} 坐标=({cx},{cy})")

            cv2.imshow('Detection', vis)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                logger.info("检测结束，用户主动退出。")
                break

    finally:
        grabber.stop()
        cap.release()
        cv2.destroyAllWindows()
        logger.info("视频资源已释放。")


if __name__ == '__main__':
    main()
