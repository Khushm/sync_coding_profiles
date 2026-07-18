class Solution:
    def rearrangeString(self, s: str, x: str, y: str) -> str:
        y_str = ""
        x_str = ""
        ans = ""
        for a in s:
            if a == y:
                y_str += a
            elif a == x:
                x_str += a
            else:
                ans += a
        if y_str:
            ans += y_str
        if x_str:
            ans += x_str
        return ans
            
            
        