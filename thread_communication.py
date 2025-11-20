#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多线程学习示例 - 线程间通信篇
此示例演示了Python中多线程之间的各种通信方式
"""

import threading
import queue
import multiprocessing
import time
import random


def queue_example():
    """
    队列（Queue）示例
    线程安全的队列，用于线程间安全地交换数据
    """
    print("\n===== 队列（Queue）通信示例 =====")
    
    # 创建队列，最大容量为10
    # Queue是线程安全的，可以被多个线程同时访问
    message_queue = queue.Queue(maxsize=10)
    
    def producer():
        """生产者线程，向队列添加消息"""
        for i in range(1, 11):
            message = f"消息-{i}"
            try:
                # 向队列添加消息，如果队列已满则阻塞
                message_queue.put(message, block=True, timeout=1)
                print(f"生产者: 添加 {message} 到队列，当前队列大小: {message_queue.qsize()}")
            except queue.Full:
                print(f"生产者: 队列已满，无法添加 {message}")
            
            # 模拟生产间隔
            time.sleep(random.uniform(0.1, 0.5))
    
    def consumer():
        """消费者线程，从队列获取消息"""
        messages_received = 0
        while messages_received < 10:
            try:
                # 从队列获取消息，如果队列为空则阻塞
                message = message_queue.get(block=True, timeout=2)
                print(f"消费者: 接收到 {message}，当前队列大小: {message_queue.qsize()}")
                messages_received += 1
                
                # 通知队列任务已完成
                message_queue.task_done()
            except queue.Empty:
                print("消费者: 队列为空，等待消息")
            
            # 模拟消费时间
            time.sleep(random.uniform(0.2, 0.8))
    
    # 创建并启动线程
    producer_thread = threading.Thread(target=producer)
    consumer_thread = threading.Thread(target=consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    # 等待生产者完成
    producer_thread.join()
    
    # 等待队列中的所有任务完成
    message_queue.join()
    
    consumer_thread.join()
    
    print("队列通信示例完成")


def priority_queue_example():
    """
    优先队列（PriorityQueue）示例
    按优先级排序的队列
    """
    print("\n===== 优先队列（PriorityQueue）通信示例 =====")
    
    # 创建优先队列
    # 元素格式为 (priority, data)，数字越小优先级越高
    priority_queue = queue.PriorityQueue()
    
    def priority_producer():
        """生产不同优先级的消息"""
        messages_with_priority = [
            (3, "普通任务 - 发送邮件"),
            (1, "紧急任务 - 系统崩溃"),
            (2, "重要任务 - 数据库备份"),
            (5, "低优先级任务 - 日志清理"),
            (4, "例行任务 - 生成报告")
        ]
        
        for priority, message in messages_with_priority:
            priority_queue.put((priority, message))
            print(f"生产者: 添加优先级 {priority} 的消息: {message}")
            time.sleep(0.2)
    
    def priority_consumer():
        """按优先级消费消息"""
        while not priority_queue.empty():
            priority, message = priority_queue.get()
            print(f"消费者: 处理优先级 {priority} 的消息: {message}")
            priority_queue.task_done()
            time.sleep(0.5)
    
    # 创建并启动线程
    producer_thread = threading.Thread(target=priority_producer)
    consumer_thread = threading.Thread(target=priority_consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    print("优先队列通信示例完成")


def shared_variable_example():
    """
    共享变量 + 锁 示例
    通过共享变量和锁机制实现线程间通信
    """
    print("\n===== 共享变量 + 锁 通信示例 =====")
    
    # 创建共享变量和锁
    shared_data = {"value": 0, "updated": False}
    lock = threading.Lock()
    
    def data_producer():
        """更新共享变量"""
        for i in range(1, 6):
            with lock:
                shared_data["value"] = i * 10
                shared_data["updated"] = True
                print(f"生产者: 更新共享变量为 {shared_data['value']}")
            time.sleep(1)
    
    def data_consumer():
        """读取共享变量"""
        updates_received = 0
        while updates_received < 5:
            with lock:
                if shared_data["updated"]:
                    print(f"消费者: 读取到共享变量值 {shared_data['value']}")
                    shared_data["updated"] = False  # 重置更新标志
                    updates_received += 1
            time.sleep(0.5)  # 轮询间隔
    
    # 创建并启动线程
    producer_thread = threading.Thread(target=data_producer)
    consumer_thread = threading.Thread(target=data_consumer)
    
    producer_thread.start()
    consumer_thread.start()
    
    producer_thread.join()
    consumer_thread.join()
    
    print("共享变量通信示例完成")


def pipe_example():
    """
    管道（Pipe）示例
    虽然主要用于多进程，但也可以用于多线程间的双向通信
    """
    print("\n===== 管道（Pipe）通信示例 =====")
    
    # 创建管道，返回两个连接对象(conn1, conn2)
    parent_conn, child_conn = multiprocessing.Pipe()
    
    def pipe_server(conn):
        """管道服务器端，接收并响应消息"""
        for i in range(5):
            # 接收消息
            message = conn.recv()
            print(f"服务器: 收到消息 '{message}'")
            
            # 发送响应
            response = f"已处理: {message} ({i+1})"
            conn.send(response)
            
            time.sleep(0.5)
    
    def pipe_client(conn):
        """管道客户端，发送消息并接收响应"""
        for i in range(5):
            message = f"客户端请求 #{i+1}"
            # 发送消息
            conn.send(message)
            print(f"客户端: 发送消息 '{message}'")
            
            # 接收响应
            response = conn.recv()
            print(f"客户端: 收到响应 '{response}'")
            
            time.sleep(0.5)
    
    # 创建并启动线程
    server_thread = threading.Thread(target=pipe_server, args=(parent_conn,))
    client_thread = threading.Thread(target=pipe_client, args=(child_conn,))
    
    server_thread.start()
    client_thread.start()
    
    server_thread.join()
    client_thread.join()
    
    # 关闭管道连接
    parent_conn.close()
    child_conn.close()
    
    print("管道通信示例完成")


def event_communication_example():
    """
    事件（Event）通信示例
    使用事件进行线程间的信号通知
    """
    print("\n===== 事件（Event）通信示例 =====")
    
    # 创建事件对象
    data_ready = threading.Event()
    data_processed = threading.Event()
    
    # 共享数据
    shared_data = None
    
    def data_generator():
        """数据生成器线程"""
        for i in range(1, 4):
            # 生成数据
            global shared_data
            shared_data = f"生成的数据 #{i}"
            print(f"生成器: 生成数据 '{shared_data}'")
            
            # 通知数据已准备好
            data_ready.set()
            
            # 等待数据处理完成
            data_processed.wait()
            data_processed.clear()  # 重置事件
            
            time.sleep(1)
    
    def data_processor():
        """数据处理器线程"""
        for i in range(1, 4):
            # 等待数据准备好
            data_ready.wait()
            
            # 处理数据
            print(f"处理器: 处理数据 '{shared_data}'")
            
            # 重置数据准备事件
            data_ready.clear()
            
            # 通知数据处理完成
            data_processed.set()
    
    # 创建并启动线程
    generator_thread = threading.Thread(target=data_generator)
    processor_thread = threading.Thread(target=data_processor)
    
    generator_thread.start()
    processor_thread.start()
    
    generator_thread.join()
    processor_thread.join()
    
    print("事件通信示例完成")


def message_passing_example():
    """
    基于队列的复杂消息传递示例
    展示如何实现简单的消息传递系统
    """
    print("\n===== 基于队列的复杂消息传递示例 =====")
    
    # 定义消息类型
    class Message:
        def __init__(self, msg_type, content, sender=None):
            self.msg_type = msg_type  # 消息类型
            self.content = content    # 消息内容
            self.sender = sender      # 发送者
            self.timestamp = time.time()  # 时间戳
    
    # 创建消息队列
    message_bus = queue.Queue()
    
    def message_handler():
        """消息处理中心"""
        while True:
            # 从消息总线获取消息
            message = message_bus.get()
            
            # 特殊消息类型表示退出
            if message.msg_type == "EXIT":
                print("消息处理中心: 收到退出消息，停止服务")
                message_bus.task_done()
                break
            
            # 根据消息类型处理
            print(f"消息处理中心: 收到来自 {message.sender} 的 {message.msg_type} 消息: {message.content}")
            
            # 模拟处理时间
            time.sleep(0.3)
            
            # 标记任务完成
            message_bus.task_done()
    
    def service_a():
        """服务A，发送消息"""
        for i in range(3):
            msg = Message("REQUEST", f"服务A的请求 #{i+1}", "ServiceA")
            message_bus.put(msg)
            print(f"服务A: 发送请求 #{i+1}")
            time.sleep(random.uniform(0.5, 1.5))
    
    def service_b():
        """服务B，发送消息"""
        for i in range(2):
            msg = Message("NOTIFICATION", f"服务B的通知 #{i+1}", "ServiceB")
            message_bus.put(msg)
            print(f"服务B: 发送通知 #{i+1}")
            time.sleep(random.uniform(0.5, 1.5))
    
    # 创建并启动消息处理中心
    handler_thread = threading.Thread(target=message_handler, daemon=True)
    handler_thread.start()
    
    # 创建并启动服务线程
    service_a_thread = threading.Thread(target=service_a)
    service_b_thread = threading.Thread(target=service_b)
    
    service_a_thread.start()
    service_b_thread.start()
    
    # 等待服务完成
    service_a_thread.join()
    service_b_thread.join()
    
    # 发送退出消息
    exit_message = Message("EXIT", "退出消息处理中心", "Main")
    message_bus.put(exit_message)
    
    # 等待消息队列处理完成
    message_bus.join()
    
    print("基于队列的消息传递示例完成")


def main():
    """
    主函数，按顺序运行所有线程间通信示例
    """
    print("Python多线程学习示例 - 线程间通信篇")
    
    # 运行各种通信示例
    queue_example()
    priority_queue_example()
    shared_variable_example()
    pipe_example()
    event_communication_example()
    message_passing_example()
    
    print("\n所有线程间通信示例执行完成!")


if __name__ == "__main__":
    main()