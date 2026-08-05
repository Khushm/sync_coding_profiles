class Solution:
    def findMissingElements(self, nums: List[int]) -> List[int]:
        min_val = min(nums)
        max_val = max(nums)
        num_set = set(nums)        
        return [x for x in range(min_val, max_val + 1) if x not in num_set]