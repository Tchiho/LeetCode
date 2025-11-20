import asyncio
import time
import threading
from enum import Enum

class State(Enum):
    WORK = "work"
    WAIT = "wait"

class FunctionA:
    def __init__(self):
        self.state = State.WORK
        self.count = 0
        self._lock = threading.Lock()
        self._thread = None
        self._running = False
    
    def _run(self):
        """A函数的内部实现"""
        while self._running:
            with self._lock:
                print(f"[A {time.strftime('%H:%M:%S')}] hello (状态: {self.state.value}, 计数: {self.count % 5 + 1}/5)")
                
                self.count += 1
                
                # 每5次切换状态
                if self.count % 5 == 0:
                    self.state = State.WAIT if self.state == State.WORK else State.WORK
                    print(f"[A {time.strftime('%H:%M:%S')}] 状态切换为: {self.state.value}")
            
            time.sleep(1)
    
    def start(self):
        """启动A函数"""
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print("[A] A函数已启动")
    
    def stop(self):
        """停止A函数"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)
        print("[A] A函数已停止")
    
    def get_state(self):
        """获取当前状态"""
        with self._lock:
            return self.state, self.count

class FunctionB:
    def __init__(self, function_a):
        self.function_a = function_a
        self.check_count = 0
    
    async def run(self):
        """B函数：异步函数，每隔7秒检查A状态"""
        while True:
            # 等待7秒
            await asyncio.sleep(7)
            
            self.check_count += 1
            current_state, current_count = self.function_a.get_state()
            
            print(f"[B {time.strftime('%H:%M:%S')}] 第{self.check_count}次检查 - A状态: {current_state.value}, A计数: {current_count}")
            
            if current_state == State.WAIT:
                print(f"[B {time.strftime('%H:%M:%S')}] ✨ word (检测到A处于wait状态)")

async def main():
    """主函数"""
    print("🚀 启动程序...")
    print("A函数: 普通函数，每隔1秒打印hello，每5次切换状态")
    print("B函数: 异步函数，每隔7秒检查A状态，发现wait时打印word")
    print("-" * 50)
    
    # 创建A函数实例并启动
    function_a = FunctionA()
    function_a.start()
    
    try:
        # 创建B函数实例并运行
        function_b = FunctionB(function_a)
        await function_b.run()
    except KeyboardInterrupt:
        print("\n正在停止程序...")
    finally:
        function_a.stop()

# 运行程序
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ 程序被用户中断")