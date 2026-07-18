class Solution:
    def compareBitonicSums(self, nums: list[int]) -> int:
        low = 0
        hig = len(nums)-1
        
        while low<hig:
            mid = (low+hig) // 2
            if nums[mid] > nums[mid+1]:
                hig = mid
            else:
                low = mid + 1
            
        # for i in range(1, n-1):
        #     if nums[i-1] < nums[i] and nums[i] > nums[i+1]:
        #         peak = i
        #         break
        
        ascend_sum = sum(nums[0:low+1])
        descend_sum = sum(nums[low:len(nums)])

        # print(ascend_sum, descend_sum)

        if ascend_sum > descend_sum:
            return 0
        elif ascend_sum < descend_sum:
            return 1
        else:
            return -1