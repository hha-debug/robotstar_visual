import cv2
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.family']=['Microsoft JhengHei']
from loguru import logger

def remove_vertical_stripes(img, notch_width=3, threshold_rel=0.1, exclusion_rel=0.02):
    """去除灰度图像中的垂直周期条纹噪声"""
    rows, cols = img.shape
    logger.info(f"图像大小: {rows} x {cols}")

    # --- 1. 计算列平均 profile 并做 FFT ---
    logger.info("检测条纹频率（对列平均进行一维 FFT）...")
    profile = img.mean(axis=0)
    fft_profile = np.fft.fft(profile)
    fft_profile_shift = np.fft.fftshift(fft_profile)
    mag_profile = np.abs(fft_profile_shift)

    center = cols // 2
    exclusion = int(cols * exclusion_rel)
    threshold = mag_profile.max() * threshold_rel

    # 找到明显的频率峰
    peak_indices = np.where(
        (mag_profile > threshold) &
        (np.abs(np.arange(cols) - center) > exclusion)
    )[0]

    logger.info(f"检测到 {len(peak_indices)} 个条纹频率峰。")

    # --- 2. 二维 DFT ---
    logger.info("执行二维 DFT ...")
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    complex_spec = dft[:, :, 0] + 1j * dft[:, :, 1]
    fshift = np.fft.fftshift(complex_spec)

    # --- 3. 构建陷波掩膜 ---
    logger.info("构建陷波掩膜（notch mask）...")
    mask = np.ones((rows, cols), dtype=np.float32)
    w = int(max(1, notch_width))

    for idx in peak_indices:
        mask[:, max(0, idx - w):min(cols, idx + w + 1)] = 0.0

    # --- 4. 掩膜滤波并反变换 ---
    logger.info("执行屏蔽频率 + 反 DFT 还原图像 ...")
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)

    img_back = cv2.idft(
        np.dstack([np.real(f_ishift).astype(np.float32),
                   np.imag(f_ishift).astype(np.float32)]),
        flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT
    )

    restored = np.clip(img_back, 0, 255).astype(np.uint8)
    magnitude = np.log1p(np.abs(fshift))  # 给你显示频谱图用

    logger.success("去条纹完成！")

    return restored, magnitude


# ======================================================
# 主程序
# ======================================================
if __name__ == "__main__":
    img_path = r"D:\robotstar__visual\2\2\3-1-4.png"

    logger.info("读取图像...")
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        logger.error("读取失败，请检查图像路径")
        raise ValueError("Invalid image path")

    logger.info("开始去除垂直条纹噪声...")
    restored, magnitude = remove_vertical_stripes(img)

    # --- 显示结果 ---
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    plt.title("原始图像")
    plt.imshow(img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("去条纹后图像")
    plt.imshow(restored, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("频谱图（log 频谱）")
    plt.imshow(magnitude, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()

    logger.info("程序结束。")

