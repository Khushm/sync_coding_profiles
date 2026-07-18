class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        m_l = len(grid)
        n_l = len(grid[0])

        visited_status = [[False for i in range(n_l)] for j in range(m_l)]
        ans = 0
        
        def check_bounds(m1, n1):
            return min(m1, n1) >= 0 and m1 < m_l and n1 < n_l

        for row in range(m_l):
            for col in range(n_l):
                if grid[row][col] == '1' and not visited_status[row][col]:
                    ans += 1
                    visited_status[row][col] = True
                    queue = deque([(row, col)])
                    
                    while queue:
                        m, n = queue.popleft()
                        nei = [(m, n-1), (m, n+1), (m-1, n), (m+1, n)] 
                        # (m-1, n-1), (m+1, n+1), (m+1, n-1), (m-1, n+1)]
                        for m1, n1 in nei:
                            if check_bounds(m1, n1) and grid[m1][n1] == '1' and not visited_status[m1][n1]:
                                visited_status[m1][n1] = True
                                queue.append((m1, n1))
        return ans