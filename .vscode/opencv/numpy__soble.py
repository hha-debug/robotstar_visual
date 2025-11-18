import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def read_image(image_path):
    """读取图像并返回numpy数组"""
    if os.path.exists(image_path):
        img = Image.open(image_path)
        return np.array(img)
    else:
        print(f"图像文件 {image_path} 不存在，创建测试图像")
        return create_test_image()

def show_image(image, title='Image', cmap=None):
    """显示图像"""
    plt.figure(figsize=(8, 6))
    if len(image.shape) == 2:  # 灰度图
        plt.imshow(image, cmap=cmap or 'gray')
    else:  # 彩色图
        plt.imshow(image)
    plt.title(title)
    plt.axis('off')
    plt.colorbar() if cmap and cmap != 'gray' else None
    plt.tight_layout()
    plt.show()

def create_test_image():
    """创建一个包含简单几何形状的测试图像"""
    image = np.zeros((200, 200), dtype=np.uint8)
    
    # 添加一个矩形
    image[50:100, 50:100] = 255
    
    # 添加一个圆形
    center = (150, 150)
    radius = 25
    y, x = np.ogrid[:200, :200]
    mask = (x - center[0])**2 + (y - center[1])**2 <= radius**2
    image[mask] = 255
    
    # 添加一些噪声
    noise = np.random.randint(0, 30, (200, 200))
    image = np.clip(image + noise, 0, 255)
    
    return image

def rgb_to_grayscale(image):
    """将RGB图像转换为灰度图"""
    if len(image.shape) == 3:
        # 使用标准的灰度转换公式: 0.299*R + 0.587*G + 0.114*B
        return np.dot(image[...,:3], [0.299, 0.587, 0.114]).astype(np.uint8)
    else:
        return image

def grayscale_to_binary(image,threshold = 128):
    '''将灰度图转换为黑白图'''
    binary_image = np.zeros_like(image)
    
    # 获取图像尺寸
    height, width = image.shape

    for i in range(height):
        for j in range(width):
            if image[i, j] > threshold:
                binary_image[i, j] = 255  # 白色
            else:
                binary_image[i, j] = 0    # 黑色
    
    return binary_image

def create_sobel_kernels():
    """创建Sobel算子的x和y方向卷积核"""
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]], dtype=np.float32)
    
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]], dtype=np.float32)
    
    return sobel_x, sobel_y

def convolve2d(image, kernel):
    """使用滑动窗口进行2D卷积"""
    kernel_height, kernel_width = kernel.shape
    image_height, image_width = image.shape
    
    # 计算输出图像的尺寸（考虑边界）
    output_height = image_height - kernel_height + 1
    output_width = image_width - kernel_width + 1
    
    # 创建输出图像
    output = np.zeros((output_height, output_width))
    
    # 滑动窗口卷积
    for i in range(output_height):
        for j in range(output_width):
            # 提取当前窗口
            window = image[i:i+kernel_height, j:j+kernel_width]
            # 计算卷积结果
            output[i, j] = np.sum(window * kernel)
    
    return output

def normalize_image(image):
    """将图像归一化到0-255范围"""
    # 找到最小值和最大值
    min_val = np.min(image)
    max_val = np.max(image)
    
    # 避免除以零
    if max_val == min_val:
        return np.zeros_like(image, dtype=np.uint8)
    
    # 归一化到0-255
    normalized = ((image - min_val) / (max_val - min_val) * 255).astype(np.uint8)
    return normalized

def sobel_edge_detection(image):
    """Sobel边缘检测主函数"""
    # 转换为灰度图
    if len(image.shape) == 3:
        gray_image = rgb_to_grayscale(image)
    else:
        gray_image = image
    
    # 创建Sobel卷积核
    sobel_x, sobel_y = create_sobel_kernels()
    
    # 在x和y方向进行卷积
    gradient_x = convolve2d(gray_image.astype(np.float32), sobel_x)
    gradient_y = convolve2d(gray_image.astype(np.float32), sobel_y)
    
    # 计算梯度幅值
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
    
    # 归一化梯度幅值
    edges = normalize_image(gradient_magnitude)
    
    return edges, gradient_x, gradient_y

def main():
    """主函数"""
    # 尝试读取图像，如果不存在则创建测试图像
    image_path =r"D:\robotstar__visual\2\2\1-5.png"
    
    try:
        # 尝试读取图像
        original_image = read_image(image_path)
        print(f"成功读取图像，形状: {original_image.shape}")
    except Exception as e:
        print(f"读取图像失败: {e}，使用测试图像")
        original_image = create_test_image()
    
    # 显示原始图像
    show_image(original_image, '原始图像')

    #显示灰度图像
    gray_img = rgb_to_grayscale(original_image)
    show_image(gray_img,'gray')

    #显示黑白图像
    binary_img = grayscale_to_binary(gray_img)
    show_image(binary_img,'binary')
    # 进行边缘检测
    edges, grad_x, grad_y = sobel_edge_detection(original_image)
    
    # 显示边缘检测结果
    show_image(edges, 'Sobel边缘检测结果')
    
    '''# 显示梯度信息
    show_image(normalize_image(grad_x), 'X方向梯度', cmap='seismic')
    show_image(normalize_image(grad_y), 'Y方向梯度', cmap='seismic')'''
    
    # 打印统计信息
    print(f"原始图像范围: [{original_image.min()}, {original_image.max()}]")
    print(f"边缘图像范围: [{edges.min()}, {edges.max()}]")
    print(f"X梯度范围: [{grad_x.min():.2f}, {grad_x.max():.2f}]")
    print(f"Y梯度范围: [{grad_y.min():.2f}, {grad_y.max():.2f}]")
    plt.show()
    
if __name__ == "__main__":
    main()