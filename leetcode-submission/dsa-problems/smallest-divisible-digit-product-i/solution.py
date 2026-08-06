class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        x = n
        while True:
            product = 1
            temp = x
            while temp > 0:
                product *= (temp % 10)
                temp //= 10
                
            if product % t == 0:
                return x
                
            x += 1