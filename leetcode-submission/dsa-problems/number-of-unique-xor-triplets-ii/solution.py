class Solution:
    def uniqueXorTriplets(self, nums: List[int]) -> int:
        n = len(nums)
        pair_xors = set()
        
        for i in range(n):
            for j in range(i, n):
                pair_xors.add(nums[i] ^ nums[j])
        
        unique_nums = set(nums)
        triplet_xors = set()
        
        for p_xor in pair_xors:
            for num in unique_nums:
                triplet_xors.add(p_xor ^ num)
                
        return len(triplet_xors)