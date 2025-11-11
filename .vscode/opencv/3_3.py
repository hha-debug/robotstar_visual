import cv2
import numpy as np
from loguru import logger

# 配置日志：输出到控制台和文件，设置格式和级别
logger.add(
    "detection_log.log",  # 日志文件路径
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",  # 日志格式
    level="INFO",  # 日志级别（DEBUG/INFO/WARNING/ERROR）
    rotation="10 MB",  # 日志文件超过10MB自动分割
    retention="7 days"  # 日志保留7天
)

def detect_color_target(image_path, target_color="red", min_area=100):
    """
    基于颜色特征检测目标并标记
    :param image_path: 原图路径
    :param target_color: 目标颜色（支持 red/blue/green 等）
    :param min_area: 最小轮廓面积（过滤小噪点）
    :return: 处理后的图像
    """
    try:
        # 1. 读取原图
        logger.info(f"开始读取图像：{image_path}")
        img = cv2.imread(image_path)
        if img is None:
            logger.error(f"无法读取图像，请检查路径：{image_path}")
            raise FileNotFoundError(f"图像路径不存在：{image_path}")
        logger.success(f"图像读取成功，尺寸：{img.shape[0]}x{img.shape[1]}")

        # 2. 转换到HSV颜色空间
        logger.debug("将图像从BGR转换到HSV颜色空间")
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 3. 定义目标颜色的HSV范围（可根据需要扩展更多颜色）
        logger.debug(f"设置目标颜色 {target_color} 的HSV阈值范围")
        color_ranges = {
            "red": [
                (np.array([0, 120, 70]), np.array([10, 255, 255])),  # 红色低范围
                (np.array([170, 120, 70]), np.array([180, 255, 255]))  # 红色高范围
            ],
            "blue": [
                (np.array([100, 120, 70]), np.array([130, 255, 255]))
            ],
            "green": [
                (np.array([40, 40, 40]), np.array([70, 255, 255]))
            ]
        }

        if target_color not in color_ranges:
            logger.warning(f"不支持的颜色 {target_color}，默认使用红色")
            target_color = "red"

        # 4. 生成颜色掩码
        masks = []
        for lower, upper in color_ranges[target_color]:
            mask = cv2.inRange(hsv, lower, upper)
            masks.append(mask)
        mask = np.bitwise_or.reduce(masks)  # 合并多个颜色区间的掩码
        logger.debug("颜色掩码生成完成")

        # 5. 形态学操作去除噪点
        logger.debug("执行形态学操作去除噪点")
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # 闭运算 填充空洞
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)   # 开运算 去除小噪点

        # 6. 检测轮廓并标记
        logger.debug("开始检测目标轮廓")
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        target_count = 0  # 统计检测到的目标数量

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < min_area:
                logger.debug(f"过滤小面积轮廓（面积：{area:.2f} < {min_area}）")
                continue
            # 绘制外接矩形
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            target_count += 1
            logger.info(f"检测到目标，位置：({x}, {y})，大小：{w}x{h}，面积：{area:.2f}")

        logger.success(f"目标检测完成，共检测到 {target_count} 个目标")

        # 7. 保存结果
        output_path = "检测结果.jpg"
        cv2.imwrite(output_path, img)
        logger.info(f"检测结果已保存至：{output_path}")

        return img

    except Exception as e:
        logger.error(f"检测过程出错：{str(e)}", exc_info=True)  # 记录详细错误堆栈
        return None

if __name__ == "__main__":
    image_path = r"D:\robotstar__visual\2\2\3-1-3.jpg"
    # 调用检测函数（可指定目标颜色，如 "blue"、"green"）
    result_img = detect_color_target(image_path, target_color="red")

    # 显示结果（如果成功）
    if result_img is not None:
        cv2.imshow("img", result_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()