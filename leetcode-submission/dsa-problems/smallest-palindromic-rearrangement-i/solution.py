class Solution:
    def smallestPalindrome(self, s: str) -> str:
        n = len(s)
        half_len = n // 2        
        first_half = sorted(s[:half_len])
        first_half_str = "".join(first_half)        
        mid = s[half_len] if n % 2 != 0 else ""        
        return first_half_str + mid + first_half_str[::-1]