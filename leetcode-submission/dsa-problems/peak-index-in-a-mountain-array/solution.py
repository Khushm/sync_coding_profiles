class Solution:
    def peakIndexInMountainArray(self, arr: List[int]) -> int:
        low = 0
        hig = len(arr) - 1
        while low < hig:
            mid = (low+hig) // 2
            if arr[mid] > arr[mid+1]:
                hig = mid
            else:
                low = mid + 1
        return low
        