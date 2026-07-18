class Solution:
    def findPeakElement(self, nums: List[int]) -> int:
        low = 0
        hig = len(nums) - 1

        while low < hig:
            mid = (low+hig) // 2
            if nums[mid] > nums[mid+1]:
                hig = mid
            else:
                low = mid + 1 
        return low

# [1,2,3,1]
