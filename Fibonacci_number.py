class Solution:
    '''递归解法'''
    # def fib(self, n: int) -> int:
    #     if n <= 1:
    #         return n
    #     if n > 1:
    #         return self.fib(n-1) + self.fib(n-2)

    '''数组解法'''
    def fib(self, n: int) -> int:
        if n == 0:
            return 0  # 特判 n = 0
        if n == 1:
            return 1  # 特判 n = 1
        temp = list((n+1)*[0])
        if n >=2:
            for index in range(2,n+1):
                temp[index] = temp[index - 1] + temp[index - 2]
        return temp[n]
    
if __name__ == "__main__":
    s = Solution()
    print(s.fib(0))