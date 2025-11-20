#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程学习示例 - 线程池篇
此示例演示了Python中concurrent.futures模块的ThreadPoolExecutor的使用方法
"""

import concurrent.futures
import time
import random


def task_function(task_id, sleep_time):
    """
    模拟耗时任务的函数
    
    参数:
        task_id: 任务ID
        sleep_time: 模拟任务执行时间（秒）
    
    返回:
        包含任务ID和执行时间的字典
    """
    print(f"任务 {task_id} 开始执行，预计耗时 {sleep_time:.2f}秒")
    time.sleep(sleep_time)
    result = {"task_id": task_id, "sleep_time": sleep_time, "completed": True}
    print(f"任务 {task_id} 执行完成")
    return result


def basic_thread_pool_example():
    """
    基础线程池示例
    展示如何创建线程池并提交任务
    """
    print("\n===== 基础线程池示例 =====")
    
    # 创建线程池，设置最大线程数为3
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 提交任务到线程池，并获取Future对象
        future1 = executor.submit(task_function, 1, 2)
        future2 = executor.submit(task_function, 2, 3)
        future3 = executor.submit(task_function, 3, 1)
        
        # 使用result()方法获取任务结果，这会阻塞直到任务完成
        print("等待任务1完成...")
        result1 = future1.result()
        print(f"任务1结果: {result1}")
        
        print("等待任务2完成...")
        result2 = future2.result()
        print(f"任务2结果: {result2}")
        
        print("等待任务3完成...")
        result3 = future3.result()
        print(f"任务3结果: {result3}")
    
    print("基础线程池示例完成")


def thread_pool_map_example():
    """
    线程池map方法示例
    适合对多个输入应用相同的函数
    """
    print("\n===== 线程池map方法示例 =====")
    
    # 准备任务数据
    task_ids = [1, 2, 3, 4, 5]
    # 为每个任务生成随机执行时间
    sleep_times = [random.uniform(0.5, 2) for _ in task_ids]
    
    print(f"任务数据: {list(zip(task_ids, sleep_times))}")
    
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 使用map方法将函数应用到多个输入上
        # map返回结果的顺序与输入顺序相同，即使任务完成顺序不同
        results = executor.map(task_function, task_ids, sleep_times)
        
        # 处理结果
        for i, result in enumerate(results):
            print(f"第{i+1}个结果: {result}")
    
    print("线程池map方法示例完成")


def thread_pool_as_completed_example():
    """
    线程池as_completed方法示例
    按照任务完成的顺序处理结果
    """
    print("\n===== 线程池as_completed方法示例 =====")
    
    # 准备任务参数
    tasks = [(1, 2), (2, 1), (3, 3), (4, 1.5), (5, 2.5)]
    
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        # 提交所有任务并保存Future对象
        future_to_task = {executor.submit(task_function, task_id, sleep_time): 
                         (task_id, sleep_time) for task_id, sleep_time in tasks}
        
        # 使用as_completed遍历完成的Future对象
        # 任务完成后立即处理结果
        for future in concurrent.futures.as_completed(future_to_task):
            task_id, sleep_time = future_to_task[future]
            try:
                # 获取结果
                result = future.result()
                print(f"任务 ({task_id}, {sleep_time}) 结果: {result}")
            except Exception as e:
                print(f"任务 ({task_id}, {sleep_time}) 发生异常: {e}")
    
    print("线程池as_completed方法示例完成")


def thread_pool_exception_handling():
    """
    线程池异常处理示例
    展示如何处理任务中的异常
    """
    print("\n===== 线程池异常处理示例 =====")
    
    def task_with_exception(task_id):
        """可能抛出异常的任务"""
        print(f"异常任务 {task_id} 开始执行")
        if task_id % 3 == 0:
            raise ValueError(f"任务 {task_id} 故意抛出异常")
        time.sleep(1)
        return f"任务 {task_id} 成功完成"
    
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # 提交多个可能抛出异常的任务
        futures = [executor.submit(task_with_exception, i) for i in range(1, 6)]
        
        # 处理结果和异常
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                print(f"正常结果: {result}")
            except Exception as e:
                print(f"捕获到异常: {e}")
    
    print("线程池异常处理示例完成")


def thread_pool_with_timeout():
    """
    线程池超时处理示例
    展示如何为任务设置超时
    """
    print("\n===== 线程池超时处理示例 =====")
    
    # 创建线程池
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        # 提交一个耗时较长的任务
        future = executor.submit(task_function, 1, 5)
        
        try:
            # 设置超时时间为2秒
            result = future.result(timeout=2)
            print(f"任务在超时前完成: {result}")
        except concurrent.futures.TimeoutError:
            print("任务执行超时！")
    
    print("线程池超时处理示例完成")


def thread_pool_shutdown_example():
    """
    线程池关闭示例
    展示shutdown方法的使用
    """
    print("\n===== 线程池关闭示例 =====")
    
    # 手动创建线程池（不使用with语句）
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    
    # 提交任务
    futures = [executor.submit(task_function, i, 1) for i in range(1, 4)]
    
    # 关闭线程池，不再接受新任务
    # wait=True 表示等待所有已提交的任务完成
    executor.shutdown(wait=True)
    
    # 处理结果
    for i, future in enumerate(futures):
        result = future.result()
        print(f"任务{i+1}结果: {result}")
    
    print("线程池关闭示例完成")


def main():
    """
    主函数，按顺序运行所有线程池示例
    """
    print("Python多线程学习示例 - 线程池篇")
    
    # 运行各种线程池示例
    basic_thread_pool_example()
    thread_pool_map_example()
    thread_pool_as_completed_example()
    thread_pool_exception_handling()
    thread_pool_with_timeout()
    thread_pool_shutdown_example()
    
    print("\n所有线程池示例执行完成!")


if __name__ == "__main__":
    main()