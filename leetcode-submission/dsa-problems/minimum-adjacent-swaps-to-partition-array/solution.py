class Solution:
    def minAdjacentSwaps(self, nums: list[int], a: int, b: int) -> int:
        MOD = 10**9 + 7
        swaps = 0
        n = len(nums)
        
        cnt_m = 0
        cnt_r = 0
        for x in nums:
            if x < a:
                swaps += (cnt_m + cnt_r)
            elif x <= b:
                swaps += cnt_r
                cnt_m += 1
            else:
                cnt_r += 1

        return (swaps) % MOD