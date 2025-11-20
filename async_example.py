import asyncio
import time

# 模拟一个耗时的IO操作，如网络请求或文件读写
async def fetch_data(delay, data_id):
    """
    模拟从某处获取数据的异步函数
    
    参数:
    delay: 模拟的延迟时间（秒）
    data_id: 数据标识符
    
    返回:
    包含数据ID和获取时间的字典
    """
    print(f"开始获取数据 {data_id}，延迟 {delay} 秒")
    # 异步等待，不会阻塞事件循环
    await asyncio.sleep(delay)
    print(f"完成获取数据 {data_id}")
    return {"id": data_id, "time": time.strftime("%H:%M:%S"), "delay": delay}

# 定义一个异步主函数
async def main():
    """
    异步主函数，演示如何并发执行多个异步任务
    """
    print("开始执行异步任务...")
    start_time = time.time()
    
    # 方法1: 按顺序等待每个任务完成
    print("\n方法1: 顺序执行异步任务")
    task1_start = time.time()
    result1 = await fetch_data(2, "A")  # 等待2秒
    result2 = await fetch_data(3, "B")  # 等待3秒
    result3 = await fetch_data(1, "C")  # 等待1秒
    task1_end = time.time()
    print(f"顺序执行总耗时: {task1_end - task1_start:.2f}秒")
    print(f"结果: {result1}, {result2}, {result3}")
    
    # 方法2: 使用asyncio.gather并发执行多个任务
    print("\n方法2: 并发执行异步任务")
    task2_start = time.time()
    results = await asyncio.gather(
        fetch_data(2, "X"),
        fetch_data(3, "Y"),
        fetch_data(1, "Z")
    )
    task2_end = time.time()
    print(f"并发执行总耗时: {task2_end - task2_start:.2f}秒")
    print(f"结果: {results}")
    
    # 方法3: 使用asyncio.Task创建任务并等待完成
    print("\n方法3: 使用Task对象执行异步任务")
    task2_start = time.time()
    task_a = asyncio.create_task(fetch_data(2, "P"))
    task_b = asyncio.create_task(fetch_data(3, "Q"))
    task_c = asyncio.create_task(fetch_data(1, "R"))
    
    # 可以在这里做其他工作
    print("任务已创建，正在等待完成...")
    
    # 等待所有任务完成
    result_a = await task_a
    result_b = await task_b
    result_c = await task_c
    
    task2_end = time.time()
    print(f"使用Task对象总耗时: {task2_end - task2_start:.2f}秒")
    print(f"结果: {result_a}, {result_b}, {result_c}")
    
    total_time = time.time() - start_time
    print(f"\n程序总耗时: {total_time:.2f}秒")

# 运行异步主函数
if __name__ == "__main__":
    # 在Python 3.7+中，可以使用asyncio.run()函数运行异步函数
    asyncio.run(main())
    
    # 对于Python 3.6及以下版本，可以使用以下方式:
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
    # loop.close()