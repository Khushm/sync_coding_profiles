class Solution:
    def minimumPushes(self, word: str) -> int:
        freqs = Counter(word).values()
        sorted_freqs = sorted(freqs, reverse=True)
        ans = 0
        for i, count in enumerate(sorted_freqs):
            pushes = (i // 8) + 1
            ans += count * pushes
            
        return ans