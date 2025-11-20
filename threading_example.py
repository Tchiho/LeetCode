#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程学习示例 - 基础篇
此示例演示了Python中threading模块的基本使用方法
"""

import threading
import time


def worker_function(worker_id, sleep_time):
    """
    工作线程函数，模拟执行任务
    
    参数:
        worker_id: 线程ID
        sleep_time: 模拟工作的睡眠时间（秒）
    """
    print(f"线程 {worker_id} (名称: {threading.current_thread().name}) 开始执行")
    # 模拟工作过程
    time.sleep(sleep_time)
    print(f"线程 {worker_id} 执行完成，总耗时: {sleep_time}秒")


def basic_threading_example():
    """
    基础线程创建和启动示例
    """
    print("\n===== 基础线程创建示例 =====")
    
    # 获取当前线程信息
    main_thread = threading.current_thread()
    print(f"主线程: {main_thread.name}, ID: {main_thread.ident}")
    
    # 创建线程对象
    # target参数指定线程要执行的函数
    # args参数传递给target函数的参数元组
    thread1 = threading.Thread(target=worker_function, args=(1, 2))
    thread2 = threading.Thread(target=worker_function, args=(2, 3))
    
    # 启动线程
    thread1.start()
    thread2.start()
    
    # 等待线程完成
    # 如果不使用join，主线程可能会在子线程完成之前结束
    thread1.join()
    thread2.join()
    
    print("所有线程执行完成")


def named_threads_example():
    """
    命名线程示例
    通过name参数为线程指定名称
    """
    print("\n===== 命名线程示例 =====")
    
    # 创建命名线程
    thread1 = threading.Thread(target=worker_function, 
                             args=(1, 1.5), 
                             name="工作线程-A")
    thread2 = threading.Thread(target=worker_function, 
                             args=(2, 2.5), 
                             name="工作线程-B")
    
    print(f"创建的线程1名称: {thread1.name}")
    print(f"创建的线程2名称: {thread2.name}")
    
    # 启动线程
    thread1.start()
    thread2.start()
    
    # 等待线程完成
    thread1.join()
    thread2.join()
    
    print("命名线程示例完成")


def daemon_threads_example():
    """
    守护线程示例
    守护线程会在主线程结束时自动终止
    """
    print("\n===== 守护线程示例 =====")
    
    # 创建非守护线程和守护线程
    normal_thread = threading.Thread(target=worker_function, 
                                  args=("普通", 5))
    daemon_thread = threading.Thread(target=worker_function, 
                                  args=("守护", 10), 
                                  daemon=True)
    
    print(f"普通线程守护状态: {normal_thread.daemon}")
    print(f"守护线程守护状态: {daemon_thread.daemon}")
    
    # 启动线程
    normal_thread.start()
    daemon_thread.start()
    
    # 只等待普通线程完成
    normal_thread.join()
    
    print("主线程结束 - 守护线程会被自动终止，即使它还没完成")


def thread_status_example():
    """
    线程状态检查示例
    演示如何检查线程是否存活
    """
    print("\n===== 线程状态检查示例 =====")
    
    # 创建线程
    thread = threading.Thread(target=worker_function, args=(1, 3))
    
    # 检查线程启动前的状态
    print(f"线程启动前存活状态: {thread.is_alive()}")
    
    # 启动线程
    thread.start()
    
    # 检查线程启动后的状态
    print(f"线程启动后存活状态: {thread.is_alive()}")
    
    # 等待线程完成
    thread.join()
    
    # 检查线程完成后的状态
    print(f"线程完成后存活状态: {thread.is_alive()}")


def main():
    """
    主函数，按顺序运行所有示例
    """
    print("Python多线程学习示例 - 基础篇")
    
    # 运行各种示例
    basic_threading_example()
    named_threads_example()
    daemon_threads_example()
    thread_status_example()
    
    print("\n所有示例执行完成!")


if __name__ == "__main__":
    main()