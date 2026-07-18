class Solution:
    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        # using bfs
        n = len(isConnected)
        
        visited = [False] * n
        
        ans = 0
                    
        
        for i in range(n):
            if visited[i]:
                continue
            queue = deque([i])
            ans+=1
            visited[i] = True
            
            while queue:
                node = queue.popleft()
                for nei in range(n):
                    if isConnected[node][nei] == 1 and not visited[nei]:
                        visited[nei] = True
                        queue.append(nei)
        return ans
        