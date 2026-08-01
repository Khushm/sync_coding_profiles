from functools import lru_cache
class Solution:
    def predictTheWinner(self, nums: List[int]) -> bool:
        @lru_cache(None)
        def dp(left, right):
            if left == right:
                return nums[left]

            pickLeft = nums[left] - dp(left + 1, right)
            pickRight = nums[right] - dp(left, right - 1)

            return max(pickLeft, pickRight)

        return dp(0, len(nums) - 1) >= 0