class Solution:
    def stoneGameIII(self, stoneValue: List[int]) -> str:
        n = len(stoneValue)
        dp = [0] * (n + 1)
        
        for i in range(n - 1, -1, -1):
            max_diff = float('-inf')
            current_sum = 0
            
            for x in range(1, 4):
                if i + x <= n:
                    current_sum += stoneValue[i + x - 1]
                    max_diff = max(max_diff, current_sum - dp[i + x])
                    
            dp[i] = max_diff
            
        if dp[0] > 0:
            return "Alice"
        elif dp[0] < 0:
            return "Bob"
        else:
            return "Tie"