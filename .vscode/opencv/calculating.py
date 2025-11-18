"""
数值计算性能测试程序
比较单线程、多线程、多进程的数值计算性能
计算1到10000000的所有整数的平方根和平方的叠加和
"""

import time
import threading
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import math

def calculate_chunk(start, end):
    """
    计算指定范围内的平方根和平方的叠加和
    
    Args:
        start: 起始数字
        end: 结束数字
    
    Returns:
        float: 计算结果的累加和
    """
    result = 0.0
    # 遍历指定范围内的每个整数
    for i in range(start, end + 1):
        # 计算每个数的平方根和平方，并累加到结果中
        result += math.sqrt(i) + i * i
    return result

def single_thread_calculation(n):
    """
    单线程计算
    
    Args:
        n: 计算范围上限
    
    Returns:
        tuple: (计算结果, 耗时)
    """
    print("开始单线程计算...")
    start_time = time.time()
    
    # 直接调用计算函数处理整个范围
    result = calculate_chunk(1, n)
    
    end_time = time.time()
    return result, end_time - start_time

def multi_thread_calculation(n, num_threads=4):
    """
    多线程计算
    
    Args:
        n: 计算范围上限
        num_threads: 线程数量
    
    Returns:
        tuple: (计算结果, 耗时)
    """
    print(f"开始多线程计算 (线程数: {num_threads})...")
    start_time = time.time()
    
    # 将任务分割成多个块，便于分配给不同线程
    chunk_size = n // num_threads  # 计算每个线程处理的数据块大小
    chunks = []  # 存储每个线程的数据范围
    
    for i in range(num_threads):
        start = i * chunk_size + 1  # 当前线程起始位置
        if i == num_threads - 1:  # 最后一个线程处理剩余部分
            end = n
        else:
            end = (i + 1) * chunk_size  # 当前线程结束位置
        chunks.append((start, end))
    
    # 使用线程池执行任务
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        # 提交所有任务到线程池
        futures = [executor.submit(calculate_chunk, start, end) for start, end in chunks]
        # 获取所有任务的结果
        results = [future.result() for future in futures]
    
    # 合并所有线程的计算结果
    total_result = sum(results)
    
    end_time = time.time()
    return total_result, end_time - start_time

def multi_process_calculation(n, num_processes=4):
    """
    多进程计算
    
    Args:
        n: 计算范围上限
        num_processes: 进程数量
    
    Returns:
        tuple: (计算结果, 耗时)
    """
    print(f"开始多进程计算 (进程数: {num_processes})...")
    start_time = time.time()
    
    # 将任务分割成多个块，便于分配给不同进程
    chunk_size = n // num_processes  # 计算每个进程处理的数据块大小
    chunks = []  # 存储每个进程的数据范围
    chunks = [(i * chunk_size + 1, (i + 1) * chunk_size if i != num_processes - 1 else n) for i in range(num_processes)]
    
    # 使用进程池执行任务
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        # 提交所有任务到进程池
        futures = [executor.submit(calculate_chunk, start, end) for start, end in chunks]
        # 获取所有任务的结果
        results = [future.result() for future in futures]
    
    # 合并所有进程的计算结果
    total_result = sum(results)
    
    end_time = time.time()
    return total_result, end_time - start_time

def format_number(num):
    """
    格式化大数字显示，便于阅读
    
    Args:
        num: 需要格式化的数字
    
    Returns:
        str: 格式化后的字符串
    """
    if num >= 1e12:
        return f"{num/1e12:.2f}万亿"
    elif num >= 1e8:
        return f"{num/1e8:.2f}亿"
    elif num >= 1e4:
        return f"{num/1e4:.2f}万"
    else:
        return str(num)

def smart_verification(results):
    """智能验证，考虑浮点数精度"""
    max_diff = max(results) - min(results)
    avg_value = sum(results) / len(results)
    
    # 计算相对差异
    relative_diff = max_diff / abs(avg_value) if avg_value != 0 else float('inf')
    
    print(f"结果范围: [{min(results):.2e}, {max(results):.2e}]")
    print(f"最大绝对差异: {max_diff:.2e}")
    print(f"相对差异: {relative_diff:.2e}")
    
    # 使用相对容差判断
    absolute_tolerance = 1e6  # 绝对容差，根据实际情况调整
    relative_tolerance = 1e-10  # 相对容差
    
    is_consistent = (max_diff < absolute_tolerance) or (relative_diff < relative_tolerance)
    
    print(f"一致性判断:")
    print(f"  - 绝对容差检查: {max_diff:.2e} < {absolute_tolerance} = {max_diff < absolute_tolerance}")
    print(f"  - 相对容差检查: {relative_diff:.2e} < {relative_tolerance} = {relative_diff < relative_tolerance}")
    print(f"结果一致: {is_consistent}")
    
    return is_consistent

def main():
    """
    主函数 - 组织整个测试流程
    """
    print("=== 数值计算性能测试程序 ===")
    print("计算1到N的所有整数的平方根和平方的叠加和")
    print("公式: Σ(sqrt(i) + i^2) for i = 1 to N")
    
    # 设置计算范围
    n = 10000000  # 1千万
    print(f"\n计算范围: 1 到 {format_number(n)}")
    print(f"预计计算量: {format_number(n)} 次运算")
    
    # 根据CPU核心数动态调整线程/进程数
    cpu_count = multiprocessing.cpu_count()  # 获取CPU核心数
    num_threads = min(8, cpu_count)  # 限制最大线程数
    num_processes = min(8, cpu_count)  # 限制最大进程数
    
    print(f"CPU核心数: {cpu_count}")
    print(f"测试线程数: {num_threads}")
    print(f"测试进程数: {num_processes}")
    
    print("\n" + "="*60)
    
    # 单线程测试 - 基准性能
    result_single, time_single = single_thread_calculation(n)
    print(f"单线程耗时: {time_single:.2f} 秒")
    print(f"单线程结果: {result_single:.2f}")
    
    print("\n" + "="*60)
    
    # 多线程测试 - 测试线程并行性能
    result_thread, time_thread = multi_thread_calculation(n, num_threads)
    print(f"多线程耗时: {time_thread:.2f} 秒 (线程数: {num_threads})")
    print(f"多线程结果: {result_thread:.2f}")
    
    print("\n" + "="*60)
    
    # 多进程测试 - 测试进程并行性能（避免GIL限制）
    result_process, time_process = multi_process_calculation(n, num_processes)
    print(f"多进程耗时: {time_process:.2f} 秒 (进程数: {num_processes})")
    print(f"多进程结果: {result_process:.2f}")
    
    # 验证结果一致性
    print("\n" + "="*60)
    print("结果验证:")
    print(f"单线程结果: {result_single:.2f}")
    print(f"多线程结果: {result_thread:.2f}")
    print(f"多进程结果: {result_process:.2f}")
    
    # 检查结果是否一致（考虑浮点数精度误差）
    results = [result_single, result_thread, result_process]
    max_diff = max(results)-min(results)  # 计算最大差异

    # 使用智能验证
    is_consistent = smart_verification(results)
    print(f"最大差异: {max_diff:.2e}")
    print(f"结果一致: {is_consistent}")  # 判断结果是否在允许误差范围内
    
    # 性能对比分析
    print("\n" + "="*60)
    print("性能对比:")
    print(f"单线程: {time_single:.2f} 秒")
    print(f"多线程: {time_thread:.2f} 秒 (加速比: {time_single/time_thread:.2f}x)")
    print(f"多进程: {time_process:.2f} 秒 (加速比: {time_single/time_process:.2f}x)")
    
    # 找出最快的方法
    times = [time_single, time_thread, time_process]
    methods = ["单线程", "多线程", "多进程"]
    fastest_idx = times.index(min(times))  # 找到最小时间的索引
    print(f"\n最快方法: {methods[fastest_idx]}")
    
    # 性能分析
    print("\n" + "="*60)
    print("性能分析:")
    print(f"单线程效率: {n/time_single:.0f} 次运算/秒")
    print(f"多线程效率: {n/time_thread:.0f} 次运算/秒")
    print(f"多进程效率: {n/time_process:.0f} 次运算/秒")
    
    # 理论分析 - 比较实际加速比与理论加速比
    print(f"\n理论分析:")
    print(f"多线程理论加速比: {num_threads}x (实际: {time_single/time_thread:.2f}x)")
    print(f"多进程理论加速比: {num_processes}x (实际: {time_single/time_process:.2f}x)")

    print("\n" + "="*60)
    print(f"计算范围： 1 ~ {n}")
    print(f"单线程耗时：{time_single:.2f}秒")
    print(f"多线程耗时：{time_thread:.2f}秒")
    print(f"多进程耗时：{time_process:.2f}秒")
    

# 程序入口点
if __name__ == "__main__":
    # 在Windows系统下，多进程编程需要这个保护
    # 确保多进程代码只在主模块中执行
    main()