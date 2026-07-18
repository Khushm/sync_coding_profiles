class Solution:
    def maximumValue(self, n: int, s: int, m: int) -> int:
        if n == 1:
            return s

        peaks = n // 2
        return s + m + (peaks - 1) * (m - 1)