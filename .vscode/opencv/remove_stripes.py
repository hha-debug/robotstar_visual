import cv2
import numpy as np
import matplotlib.pyplot as plt

def remove_vertical_stripes(img, notch_width=3, threshold_rel=0.1, exclusion_rel=0.02):
    """去除灰度图像中的垂直周期条纹噪声"""
    rows, cols = img.shape

    # 1. 计算列平均 profile，并对其做FFT来检测条纹频率
    profile = img.mean(axis=0)
    fft_profile = np.fft.fft(profile)
    fft_profile_shift = np.fft.fftshift(fft_profile)
    mag_profile = np.abs(fft_profile_shift)

    center = cols // 2
    exclusion = int(max(1, cols * exclusion_rel))
    threshold = mag_profile.max() * threshold_rel
    peak_indices = np.where(
        (mag_profile > threshold) & (np.abs(np.arange(cols) - center) > exclusion)
    )[0]

    # 2. 图像的二维DFT
    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    complex_spec = dft[:, :, 0] + 1j * dft[:, :, 1]
    fshift = np.fft.fftshift(complex_spec)

    # 3. 构建掩膜，屏蔽检测到的条纹频率
    mask = np.ones((rows, cols), dtype=np.float32)
    w = int(max(1, notch_width))
    for idx in peak_indices:
        l = max(0, idx - w)
        r = min(cols, idx + w + 1)
        mask[:, l:r] = 0.0

    # 4. 频谱乘mask并反变换回图像
    fshift_filtered = fshift * mask
    f_ishift = np.fft.ifftshift(fshift_filtered)
    img_back = cv2.idft(
        np.dstack([np.real(f_ishift).astype(np.float32),
                   np.imag(f_ishift).astype(np.float32)]),
        flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT
    )

    return np.clip(img_back, 0, 255).astype(np.uint8)


# ==========================
# 主程序
# ==========================
if __name__ == "__main__":
    # 读取灰度图
    img = cv2.imread(r"D:\robotstar__visual\2\2\3-1-4.png", cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("图像读取失败，请检查路径。")

    # 去除条纹
    restored = remove_vertical_stripes(img, notch_width=3, threshold_rel=0.1, exclusion_rel=0.02)

    # 显示结果
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.title("原始图像")
    plt.imshow(img, cmap="gray")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("去条纹后图像")
    plt.imshow(restored, cmap="gray")
    plt.axis("off")

    plt.tight_layout()
    plt.show()
