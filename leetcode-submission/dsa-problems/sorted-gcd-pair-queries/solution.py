class Solution:
    def gcdValues(self, nums: List[int], queries: List[int]) -> List[int]:
        mx = max(nums)
        freq = [0 for i in range(mx+1)]
        for num in nums:
            freq[num] += 1
        # print(freq)
        
        gcd_freq = [0 for i in range(mx+1)]
        for gcd in range(mx, 0, -1):
            for num in range(gcd, mx+1, gcd):
                gcd_freq[gcd] += freq[num]
            pairs = gcd_freq[gcd] * (gcd_freq[gcd] - 1) // 2
            for dups in range(2*gcd, mx+1, gcd):
                pairs -= gcd_freq[dups]
            gcd_freq[gcd] = pairs
        # print(gcd_freq)

        prefix = []
        commulative_idx = []
        running = 0
        for idx in range(len(gcd_freq)):
            if gcd_freq[idx]:
                running += gcd_freq[idx]
                prefix.append(idx)
                commulative_idx.append(running)

        ans = [-1 for i in range(len(queries))]
        for q in range(len(queries)):
            # idx = bisect_right(commulative_idx, queries[q])
            # ans[q] = prefix[idx]
            low = 0
            hig = len(commulative_idx) - 1
            while low <= hig:
                mid = (low+hig) // 2
                if queries[q] >= commulative_idx[mid]:
                    low = mid + 1
                else:
                    hig = mid - 1
            ans[q] = prefix[low]
        return ans
