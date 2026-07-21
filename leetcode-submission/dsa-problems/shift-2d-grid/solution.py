class Solution:
    def shiftGrid(self, grid: List[List[int]], k: int) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])
        t = m*n
        

        # if not k or t%k == 0:
        #     return grid
        
        k = k%t
        
        ans = [[0] * n for _ in range(m)]

        for row in range(m):
            for col in range(n):
                old_idx = row * n + col
                new_idx = (old_idx + k) % t
                new_row = new_idx // n
                new_col = new_idx % n

                ans[new_row][new_col] = grid[row][col]
        return ans
        