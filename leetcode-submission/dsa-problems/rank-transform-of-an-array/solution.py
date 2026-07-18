class Solution:
    def arrayRankTransform(self, arr: List[int]) -> List[int]:
        n = len(arr)
        if n == 0:
            return []
        if n == 1:
            return [1]

        arr1 = arr.copy()
        arr1.sort()
        hash_ = {}
        hash_[arr1[0]] = 1
        rank = 2

        for i in range(1, n):
            if arr1[i] == arr1[i-1]:
                continue
            hash_[arr1[i]] = rank
            rank += 1
        
        ans = [-1] * n
        
        for i in range(n):
            ans[i] = hash_[arr[i]]
        return ans