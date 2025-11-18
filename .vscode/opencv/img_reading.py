"""
图片读取性能测试程序
比较单线程、多线程、多进程的图片读取性能
"""

import os
import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from PIL import Image
import glob

def read_image(image_path):
    """读取单张图片
    Args:
        image_path: 图片文件路径
    Returns:
        dict: 包含图片信息或错误的字典
    """
    try:
        # 使用PIL的Image.open打开图片文件
        with Image.open(image_path) as img:
            # 获取图片基本信息并返回
            return {
                'path': image_path,      # 图片路径
                'size': img.size,        # 图片尺寸 (宽, 高)
                'mode': img.mode,        # 图片模式 (RGB, RGBA等)
                'format': img.format     # 图片格式 (JPEG, PNG等)
            }
    except Exception as e:
        # 如果读取失败，返回错误信息
        return {'path': image_path, 'error': str(e)}

def single_thread_read(image_paths):
    """单线程读取图片
    Args:
        image_paths: 图片路径列表
    Returns:
        tuple: (结果列表, 耗时)
    """
    print("开始单线程读取...")
    start_time = time.time()  # 记录开始时间
    
    results = []  # 存储读取结果的列表
    # 遍历所有图片路径
    for i, path in enumerate(image_paths):
        result = read_image(path)  # 读取单张图片
        results.append(result)     # 将结果添加到列表

    end_time = time.time()  # 记录结束时间
    return results, end_time - start_time  # 返回结果和耗时

def multi_thread_read(image_paths, max_workers=4):
    """多线程读取图片
    Args:
        image_paths: 图片路径列表
        max_workers: 最大线程数
    Returns:
        tuple: (结果列表, 耗时)
    """
    print(f"开始多线程读取 (线程数: {max_workers})...")
    start_time = time.time()  # 记录开始时间
    
    # 使用线程池执行器管理线程
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 使用map方法并行处理所有图片
        results = list(executor.map(read_image, image_paths))
    
    end_time = time.time()  # 记录结束时间
    return results, end_time - start_time  # 返回结果和耗时

def multi_process_read(image_paths, max_workers=4):
    """多进程读取图片
    Args:
        image_paths: 图片路径列表
        max_workers: 最大进程数
    Returns:
        tuple: (结果列表, 耗时)
    """
    print(f"开始多进程读取 (进程数: {max_workers})...")
    start_time = time.time()  # 记录开始时间
    
    # 使用进程池执行器管理进程
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # 使用map方法并行处理所有图片
        results = list(executor.map(read_image, image_paths))
    
    end_time = time.time()  # 记录结束时间
    return results, end_time - start_time  # 返回结果和耗时

def find_image_files(data_folder):
    """查找data文件夹中的所有图片文件
    Args:
        data_folder: 数据文件夹路径
    Returns:
        list: 图片文件路径列表
    """
    # 检查文件夹是否存在
    if not os.path.exists(data_folder):
        print(f"错误: 文件夹 '{data_folder}' 不存在")
        return []
    
    # 支持的图片格式扩展名
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.gif', '*.tiff', '*.webp']
    
    image_paths = []  # 存储找到的图片路径
    # 遍历所有图片格式
    for ext in image_extensions:
        # 使用glob模式匹配文件（递归搜索子目录）
        pattern = os.path.join(data_folder, '**', ext)
        image_paths.extend(glob.glob(pattern, recursive=True))
    
    return image_paths

def analyze_results(results, method_name):
    """分析读取结果
    Args:
        results: 读取结果列表
        method_name: 方法名称（用于显示）
    """
    total_images = len(results)  # 总图片数
    successful = sum(1 for r in results if 'error' not in r)  # 成功读取的数量
    failed = total_images - successful  # 读取失败的数量
    
    print(f"\n{method_name} 结果分析:")
    print(f"总图片数: {total_images}")
    print(f"成功读取: {successful}")
    print(f"读取失败: {failed}")
    
    # 如果有成功读取的图片，进行详细统计
    if successful > 0:
        # 统计图片格式分布
        formats = {}
        sizes = []  # 存储所有图片尺寸
        for result in results:
            if 'error' not in result:
                fmt = result.get('format', 'Unknown')  # 获取图片格式
                formats[fmt] = formats.get(fmt, 0) + 1  # 计数
                sizes.append(result['size'])  # 记录尺寸
        
        print(f"图片格式分布: {formats}")
        if sizes:
            print(f"图片尺寸范围: {min(sizes)} ~ {max(sizes)}")  # 显示尺寸范围

def main():
    """主函数 - 协调整个测试流程"""
    print("=== 图片读取性能测试程序 ===\n")
    
    # 查找图片文件
    data_folder =r"D:\robotstar__visual\2\2\data"
    print(f"正在搜索图片文件: {data_folder}")
    
    image_paths = find_image_files(data_folder)
    
    # 如果找不到图片，创建测试图片
    if not image_paths:
        print("未找到图片文件，创建测试图片...")
        create_test_images()
        image_paths = find_image_files(data_folder)
    
    # 如果仍然没有图片，退出程序
    if not image_paths:
        print("无法找到或创建测试图片，程序退出")
        return
    
    print(f"找到 {len(image_paths)} 张图片")
    print(f"图片文件示例: {image_paths[:3]}...")  # 显示前3个图片路径作为示例
    7
    print(f"\n开始性能测试 (测试图片数: {len(image_paths)})...")
    print("="*60)  # 分隔线
    
    # 单线程测试
    results_single, time_single = single_thread_read(image_paths)
    print(f"单线程耗时: {time_single:.2f} 秒")
    analyze_results(results_single, "单线程")
    
    print("\n" + "="*60)
    
    # 多线程测试
    thread_workers = min(4, len(image_paths))  # 线程数不超过图片数
    results_thread, time_thread = multi_thread_read(image_paths, thread_workers)
    print(f"多线程耗时: {time_thread:.2f} 秒 (线程数: {thread_workers})")
    analyze_results(results_thread, "多线程")
    
    print("\n" + "="*60)
    
    # 多进程测试
    process_workers = min(4, len(image_paths))  # 进程数不超过图片数
    results_process, time_process = multi_process_read(image_paths, process_workers)
    print(f"多进程耗时: {time_process:.2f} 秒 (进程数: {process_workers})")
    analyze_results(results_process, "多进程")
    
    # 性能对比分析
    print("\n" + "="*60)
    print("性能对比:")
    print(f"单线程: {time_single:.2f} 秒")
    # 计算加速比：单线程时间/多线程时间
    print(f"多线程: {time_thread:.2f} 秒 (加速比: {time_single/time_thread:.2f}x)")
    # 计算加速比：单线程时间/多进程时间
    print(f"多进程: {time_process:.2f} 秒 (加速比: {time_single/time_process:.2f}x)")
    
    # 找出最快的方法
    times = [time_single, time_thread, time_process]
    methods = ["单线程", "多线程", "多进程"]
    fastest_idx = times.index(min(times))  # 找到最小时间的索引
    print(f"\n最快方法: {methods[fastest_idx]}")

    print("\n" + "="*60)
    print(f"共找到 {len(image_paths)} 张图片")
    print(f"单线程耗时: {time_single:.2f} 秒")
    print(f"多线程耗时: {time_thread:.2f} 秒")
    print(f"多进程耗时: {time_process:.2f} 秒 ")
    
def create_test_images():
    """创建测试图片（如果找不到现有图片）"""
    print("创建测试图片...")
    
    # 创建测试目录
    test_dir = "二轮任务图片资料/data"
    os.makedirs(test_dir, exist_ok=True)  # 创建目录，如果已存在则不报错
    
    # 创建一些简单的测试图片
    for i in range(10):
        # 创建不同颜色的测试图片
        img = Image.new('RGB', (100, 100), color=(i*25, i*25, i*25))
        img_path = os.path.join(test_dir, f"test_image_{i:02d}.png")
        img.save(img_path)  # 保存图片
    
    print(f"已创建 10 张测试图片到 {test_dir}")

# 程序入口点
if __name__ == "__main__":
    main()