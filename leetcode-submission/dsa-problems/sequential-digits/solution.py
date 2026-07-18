class Solution:
    def sequentialDigits(self, low: int, high: int) -> List[int]:
        # ans = []
        # for start in range(1, 10):
        #     num = start
        #     for nxt in range(start + 1, 10):
        #         num = num * 10 + nxt
        #         if low <= num <= high:
        #             ans.append(num)
        # return sorted(ans)

        s = "123456789"
        ans = []
        low_len = len(str(low))
        hig_len = len(str(high)) + 1
        for width in range(low_len, hig_len):
            for start in range(10 - width):
                num = int(s[start:start+width])
                if num >= low and num <= high:
                    ans.append(num)
        return ans