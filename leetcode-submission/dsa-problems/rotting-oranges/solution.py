class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        row = len(grid)
        col = len(grid[0])

        def is_safe(i, j):
            return min(i, j) >= 0 and i < row and j < col

        def is_rotten(i, j):
            return grid[i][j] == 2
        
        def is_fresh(i, j):
            return grid[i][j] == 1
        
        visited = [[0 for j in range(col)] for i in range(row)]
        queue = deque()

        for i in range(row):
            for j in range(col):
                if is_rotten(i, j):
                    visited[i][j] = 2
                    queue.append((i, j, 0))
                elif is_fresh(i, j):
                    visited[i][j] = 1
        
        ans = 0
        dr = [1, -1, 0, 0]
        dc = [0, 0, 1, -1]

        while queue:
            r, c, t = queue.popleft()
            for i in range(4):
                nr = r + dr[i]
                nc = c + dc[i]
                if is_safe(nr, nc) and visited[nr][nc] == 1:
                    visited[nr][nc] = 2
                    queue.append((nr, nc, t+1))
                    ans = max(t+1, ans)
        
        for i in range(row):
            for j in range(col):
                if visited[i][j] == 1:
                    return -1
        # print(visited)
        return ans