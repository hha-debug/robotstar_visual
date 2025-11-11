import threading
import time

def task(name, sleep_time):
    start = time.time()
    print(f"线程 {name} 开始 at {time.time():.6f}")
    time.sleep(sleep_time)
    end = time.time()
    print(f"线程 {name} 结束 at {time.time():.6f}, 实际运行: {end-start:.6f}s")

# 创建线程
thread1 = threading.Thread(target=task, args=("A", 2.0))
thread2 = threading.Thread(target=task, args=("B", 2.0))

thread1.start()
thread2.start()

thread1.join()
thread2.join()