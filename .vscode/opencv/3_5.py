"""
实时目标检测与坐标发送示例

功能：
- 使用 OpenCV 实时从摄像头读取帧（或视频文件）
- 识别黄色（小黄鸭，id=0）和绿色（方块，id=1）目标
- 在图像上绘制最小外接矩形（旋转矩形），并在矩形附近显示 id 和中心坐标
- 在终端实时打印 id,x,y（中心点坐标）
- 在图像上显示实时帧率（FPS）
- 使用多线程（采集线程 + 主处理线程）提高实时性

依赖：opencv-python, numpy, matplotlib (可选用于调试)

运行示例：
    python 3_5.py

脚本仅读取固定视频文件路径：D:\robotstar__visual\2\2\3-2.mp4

快捷键：按 'q' 退出
"""

import time
import threading
import collections
import queue
import os
import cv2
import numpy as np


class FrameGrabber(threading.Thread):
    """Continuously grab frames from VideoCapture and push to a queue."""
    def __init__(self, cap, q, name='FrameGrabber'):
        super().__init__(daemon=True)
        self.cap = cap
        self.q = q
        self.running = True

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                # end of video or camera error
                self.running = False
                break
            # Keep only latest frame to avoid backlog
            try:
                if self.q.full():
                    _ = self.q.get_nowait()
                self.q.put_nowait(frame)
            except Exception:
                pass

    def stop(self):
        self.running = False


# SerialSender and serial functionality removed


def detect_and_annotate(frame):
    """Detect yellow and green objects and annotate frame.

    Returns:
      annotated_frame, detections, magnitude (None placeholder)
    detections: list of tuples (id, center_x, center_y, box_points)
    """
    vis = frame.copy()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    detections = []

    # -- Yellow (small yellow duck) -> id 0
    # HSV range for yellow may need tuning depending on lighting
    lower_yellow = np.array([18, 80, 80])
    upper_yellow = np.array([35, 255, 255])
    mask_y = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # morphological
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_OPEN, kernel)
    mask_y = cv2.morphologyEx(mask_y, cv2.MORPH_CLOSE, kernel)

    contours_y, _ = cv2.findContours(mask_y, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours_y:
        area = cv2.contourArea(cnt)
        if area < 200:  # filter small noise; tune as needed
            continue
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect).astype(int)
        cx, cy = int(rect[0][0]), int(rect[0][1])
        detections.append((0, cx, cy, box))

    # -- Green (green square) -> id 1
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

    # Draw detections
    for det in detections:
        id_, cx, cy, box = det
        color = (0, 255, 255) if id_ == 0 else (0, 255, 0)
        cv2.drawContours(vis, [box], 0, color, 2)
        text = f"ID:{id_} ({cx},{cy})"
        cv2.putText(vis, text, (cx - 40, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        # draw center
        cv2.circle(vis, (cx, cy), 3, (255, 0, 0), -1)

    return vis, detections


def main():
    # fixed input video file (no camera interaction)
    src = r"D:\robotstar__visual\2\2\3-2.mp4"

    cap = cv2.VideoCapture(src)
    if not cap.isOpened():
        print("Failed to open capture source")
        return

    # serial communication removed — no serial prompts or sending

    frame_q = queue.Queue(maxsize=2)
    grabber = FrameGrabber(cap, frame_q)
    grabber.start()

    fps_hist = collections.deque(maxlen=30)

    try:
        while True:
            try:
                frame = frame_q.get(timeout=1.0)
            except queue.Empty:
                if not grabber.is_alive():
                    break
                continue

            t0 = time.time()
            vis, detections = detect_and_annotate(frame)

            # compute fps
            t1 = time.time()
            fps_hist.append(1.0 / (t1 - t0) if (t1 - t0) > 0 else 0)
            fps = sum(fps_hist) / len(fps_hist) if fps_hist else 0.0

            # overlay FPS
            cv2.putText(vis, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

            # print detections and send via serial
            for det in detections:
                id_, cx, cy, _ = det
                line = f"{id_},{cx},{cy}\n"
                print(line.strip())

            cv2.imshow('Detection', vis)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        grabber.stop()
        cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
