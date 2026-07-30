class Solution:
    def smallestPalindrome(self, s: str, k: int) -> str:
        n = len(s)
        m = n // 2
        
        counts = [0] * 26
        for i in range(m):
            counts[ord(s[i]) - ord('a')] += 1
            
        def get_ways(counts, rem_len, cap):
            res = 1
            rem = rem_len
            for c in counts:
                if c > 0:
                    res *= math.comb(rem, c)
                    if res >= cap:
                        return cap
                    rem -= c
            return res

        total_ways = get_ways(counts, m, k + 1)
        if total_ways < k:
            return ""
        
        res_half = []
        for pos in range(m):
            rem_len = m - pos
            for c_idx in range(26):
                if counts[c_idx] == 0:
                    continue
                
                counts[c_idx] -= 1
                ways = get_ways(counts, rem_len - 1, k + 1)
                
                if k <= ways:
                    res_half.append(chr(ord('a') + c_idx))
                    break
                else:
                    k -= ways
                    counts[c_idx] += 1 
                    
        first_half = "".join(res_half)
        mid = s[m] if n % 2 == 1 else ""
        return first_half + mid + first_half[::-1]