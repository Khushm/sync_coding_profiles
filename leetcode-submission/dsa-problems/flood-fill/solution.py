class Solution:
    def floodFill(self, image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:
        if image[sr][sc] == color:
            return image
        
        m = len(image)
        n = len(image[0])

        # visited = [[False for j in range(n)] for i in range(m)]

        queue = deque([(sr, sc)])
        # visited[sr][sc] = True
        pixel_match = image[sr][sc]
        image[sr][sc] = color

        def is_safe(row, col):
            return min(row, col) >= 0 and row < m and col < n

        def is_same_pixel(row, col):
            return pixel_match == image[row][col]
        
        # def is_not_visited(row, col):
        #     return not visited[row][col]
        
        while queue:
            row, col = queue.popleft()
            nei = [(row+1, col), (row-1, col), (row, col+1), (row, col-1)]
            for row1, col1 in nei:
                if is_safe(row1, col1) and is_same_pixel(row1, col1):
                    #  and is_not_visited(row1, col1):
                    # visited[row1][col1] = True
                    image[row1][col1] = color
                    queue.append((row1, col1))
        return image