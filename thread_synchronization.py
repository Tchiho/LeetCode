#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程学习示例 - 线程同步机制
此示例演示了Python中常见的线程同步机制，如锁、事件、信号量等
"""

import threading
import time


# 全局变量，多个线程共享
shared_counter = 0


def lock_example():
    """
    锁（Lock）示例
    用于保护共享资源，防止竞态条件
    """
    global shared_counter
    shared_counter = 0  # 重置计数器
    
    print("\n===== 锁（Lock）示例 =====")
    
    # 创建锁对象
    lock = threading.Lock()
    
    def increment_counter(thread_id, iterations):
        """增加计数器的值"""
        global shared_counter
        
        for i in range(iterations):
            # 获取锁
            lock.acquire()
            try:
                # 临界区 - 访问共享资源
                current_value = shared_counter
                # 模拟处理时间
                time.sleep(0.001)
                shared_counter = current_value + 1
            finally:
                # 确保锁会被释放
                lock.release()
        
        print(f"线程 {thread_id} 完成，当前计数器值: {shared_counter}")
    
    # 创建多个线程
    threads = []
    num_threads = 5
    iterations_per_thread = 1000
    
    for i in range(num_threads):
        thread = threading.Thread(target=increment_counter, args=(i, iterations_per_thread))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print(f"\n所有线程完成后的计数器值: {shared_counter}")
    print(f"预期的计数器值: {num_threads * iterations_per_thread}")
    print(f"结果正确: {shared_counter == num_threads * iterations_per_thread}")


def rlock_example():
    """
    可重入锁（RLock）示例
    允许同一线程多次获取同一把锁
    """
    print("\n===== 可重入锁（RLock）示例 =====")
    
    # 创建可重入锁对象
    rlock = threading.RLock()
    
    def recursive_function(depth):
        """递归函数，演示可重入锁的使用"""
        # 获取锁
        rlock.acquire()
        try:
            print(f"递归深度 {depth} - 获取锁")
            
            # 递归终止条件
            if depth < 3:
                # 在同一线程中再次获取锁
                recursive_function(depth + 1)
            
            print(f"递归深度 {depth} - 释放锁")
        finally:
            # 释放锁
            rlock.release()
    
    # 启动线程执行递归函数
    thread = threading.Thread(target=recursive_function, args=(0,))
    thread.start()
    thread.join()
    
    print("可重入锁示例完成")


def event_example():
    """
    事件（Event）示例
    用于线程间的信号通知
    """
    print("\n===== 事件（Event）示例 =====")
    
    # 创建事件对象
    event = threading.Event()
    
    def waiter_function(thread_id):
        """等待事件的线程"""
        print(f"线程 {thread_id} 等待事件触发")
        # 等待事件被设置
        event.wait()
        print(f"线程 {thread_id} 收到事件通知，继续执行")
    
    def setter_function():
        """设置事件的线程"""
        print("设置线程: 准备触发事件...")
        # 模拟一些准备工作
        time.sleep(3)
        print("设置线程: 触发事件")
        # 触发事件，通知所有等待的线程
        event.set()
    
    # 创建等待线程
    waiter_threads = []
    for i in range(3):
        thread = threading.Thread(target=waiter_function, args=(i,))
        waiter_threads.append(thread)
        thread.start()
    
    # 创建设置线程
    setter_thread = threading.Thread(target=setter_function)
    setter_thread.start()
    
    # 等待所有线程完成
    for thread in waiter_threads:
        thread.join()
    setter_thread.join()
    
    print("事件示例完成")


def semaphore_example():
    """
    信号量（Semaphore）示例
    限制对资源的并发访问数量
    """
    print("\n===== 信号量（Semaphore）示例 =====")
    
    # 创建信号量，允许最多2个线程同时访问资源
    semaphore = threading.Semaphore(2)
    
    def resource_access(thread_id):
        """尝试访问受信号量保护的资源"""
        print(f"线程 {thread_id} 尝试访问资源")
        
        # 获取信号量
        semaphore.acquire()
        try:
            print(f"线程 {thread_id} 成功访问资源")
            # 模拟资源使用时间
            time.sleep(2)
        finally:
            # 释放信号量
            semaphore.release()
            print(f"线程 {thread_id} 释放资源")
    
    # 创建多个线程
    threads = []
    for i in range(5):
        thread = threading.Thread(target=resource_access, args=(i,))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    print("信号量示例完成")


def condition_example():
    """
    条件变量（Condition）示例
    用于线程间的复杂同步，支持等待/通知机制
    """
    print("\n===== 条件变量（Condition）示例 =====")
    
    # 创建条件变量
    condition = threading.Condition()
    
    # 共享资源
    queue = []
    MAX_ITEMS = 5
    
    def producer():
        """生产者函数，向队列添加数据"""
        for i in range(10):
            with condition:
                # 检查队列是否已满
                while len(queue) >= MAX_ITEMS:
                    print(f"队列已满（{len(queue)}/5），生产者等待")
                    condition.wait()
                
                # 添加数据到队列
                item = f"项目-{i}"
                queue.append(item)
                print(f"生产者: 添加 {item} 到队列，当前队列大小: {len(queue)}")
                
                # 通知消费者有新数据可用
                condition.notify()
                
            # 模拟生产间隔
            time.sleep(0.5)
    
    def consumer():
        """消费者函数，从队列取出数据"""
        items_consumed = 0
        
        while items_consumed < 10:
            with condition:
                # 检查队列是否为空
                while len(queue) == 0:
                    print("队列空，消费者等待")
                    condition.wait()
                
                # 从队列取出数据
                item = queue.pop(0)
                items_consumed += 1
                print(f"消费者: 取出 {item}，当前队列大小: {len(queue)}")
                
                # 通知生产者可以继续添加数据
                condition.notify()
                
            # 模拟消费时间
            time.sleep(1)
    
    # 创建生产者和消费者线程
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    # 启动线程
    producer_thread.start()
    consumer_thread.start()
    
    # 等待线程完成
    producer_thread.join()
    consumer_thread.join()
    
    print("条件变量示例完成")


def main():
    """
    主函数，按顺序运行所有线程同步示例
    """
    print("Python多线程学习示例 - 线程同步机制篇")
    
    # 运行各种同步示例
    lock_example()
    rlock_example()
    event_example()
    semaphore_example()
    condition_example()
    
    print("\n所有线程同步示例执行完成!")


if __name__ == "__main__":
    main()