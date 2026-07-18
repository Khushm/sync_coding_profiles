class Solution:
    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a%b)

    def gcdSum(self, nums: list[int]) -> int:
        n = len(nums)
        prefix_gcd = [0] * n
        mx = 0
        for idx in range(n):
            mx = max(mx, nums[idx])
            prefix_gcd[idx] = self.gcd(nums[idx], mx)
        prefix_gcd.sort()
        for idx in range(n//2):
            prefix_gcd[idx] = self.gcd(prefix_gcd[idx], prefix_gcd[n-idx-1])
        return sum(prefix_gcd[0:n//2])