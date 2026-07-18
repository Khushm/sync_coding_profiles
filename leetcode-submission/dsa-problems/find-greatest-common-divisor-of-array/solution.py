class Solution:
    def gcd(self, mini, maxi):
        if mini == 0:
            return maxi
        return self.gcd(maxi%mini, mini)

    def findGCD(self, nums: List[int]) -> int:
        mini = min(nums)
        maxi = max(nums)
        
        return self.gcd(mini, maxi)