class Solution:    
    # @lru_cache(None)
    def gcd(self, a, b):
        if b == 0:
            return a
        return self.gcd(b, a%b)

    # @lru_cache(None)
    def solve(self, nums, i, gcd1, gcd2):
        if i == len(nums):
            if gcd1 and gcd2 and gcd1 == gcd2:
                return 1
            return 0
        if self.mem[i][gcd1][gcd2] != -1:
            return self.mem[i][gcd1][gcd2]

        skip = self.solve(nums, i+1, gcd1, gcd2)
        seq1 = self.solve(nums, i+1, self.gcd(nums[i], gcd1), gcd2)
        seq2 = self.solve(nums, i+1, gcd1, self.gcd(nums[i], gcd2))
        self.mem[i][gcd1][gcd2] = (skip + seq1 + seq2) % self.MOD
        return self.mem[i][gcd1][gcd2]
    
    def subsequencePairCount(self, nums: List[int]) -> int:
        self.MOD = 10**9 + 7
        n = len(nums)
        mx = max(nums) + 1
        self.mem = [[[-1] * mx for _ in range(mx)] for _ in range(n)]
        # print(self.mem)
        # return self.solve(tuple(nums), 0, 0, 0)
        return self.solve(nums, 0, 0, 0)