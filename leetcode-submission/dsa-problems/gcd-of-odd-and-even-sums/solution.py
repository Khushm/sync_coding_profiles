class Solution:
    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a%b)

    def gcdOfOddEvenSums(self, n: int) -> int:
        sum_odd = 0
        sum_even = 0
        for i in range(2*n+1):
            if i%2 == 0:
                sum_even += i
            else:
                sum_odd += i
        print(sum_odd, sum_even)
        return self.gcd(sum_odd, sum_even)