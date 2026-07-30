class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        '''
        freq = defaultdict(int)
        for num in nums:
            freq[num] += 1
        for k, v in freq.items():
            if v == 1:
                return k
        return -1
        '''
        
        '''
        ans = 0
        for num in nums:
            ans  = ans^num
        return ans
        '''

        return reduce(lambda x, y: x^y, nums)