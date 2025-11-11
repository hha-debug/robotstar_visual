import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def read_image(image_path):
    """读取图像并返回numpy数组"""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        return np.array(img)

def gaussian_noise(image):
    h, w, c = image.shape
    mean = 0
    sigma = 25  # 标准差
    noise = np.random.normal(mean, sigma, (h, w, c)) #根据均值和标准差生成符合高斯分布的噪声
    noisy_image = np.clip(image + noise, 0, 255).astype(np.uint8)
    return noisy_image

def main():
    imge_path = r"D:\robotstar__visual\2\2\2-2.png"
    image_row = read_image(imge_path)
    noisy_image = gaussian_noise(image_row)
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(image_row)
    plt.title("Original Image")
    plt.axis("off")  # 关闭坐标轴
        
        # 显示加噪声后的图像
    plt.subplot(1, 2, 2)
    plt.imshow(noisy_image)
    plt.title("Noisy Image")
    plt.axis("off")  # 关闭坐标轴
        
    plt.show()

if __name__ == "__main__":
    main()
    