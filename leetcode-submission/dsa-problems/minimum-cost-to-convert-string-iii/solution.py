from collections import defaultdict

class Solution:
    def minCost(self, source: str, target: str, rules: list[list[str]], costs: list[int]) -> int:
        n = len(source)
        if len(target) != n:
            return -1
            
        rule_dict = defaultdict(list)
        
        best_rules = {}
        for (pat, rep), cost in zip(rules, costs):
            wildcards = pat.count('*')
            total_cost = cost + wildcards
            if (pat, rep) not in best_rules or total_cost < best_rules[(pat, rep)]:
                best_rules[(pat, rep)] = total_cost
                
        for (pat, rep), total_cost in best_rules.items():
            rule_dict[len(pat)].append((pat, rep, total_cost))
            
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        for i in range(n):
            if dp[i] == float('inf'):
                continue
                
            if source[i] == target[i]:
                if dp[i] < dp[i + 1]:
                    dp[i + 1] = dp[i]
                    
            for length, current_rules in rule_dict.items():
                if i + length > n:
                    continue
                    
                target_sub = target[i : i + length]
                source_sub = source[i : i + length]
                
                for pat, rep, total_cost in current_rules:
                    if rep != target_sub:
                        continue
                        
                    match = True
                    for j in range(length):
                        if pat[j] != '*' and pat[j] != source_sub[j]:
                            match = False
                            break
                            
                    if match:
                        if dp[i] + total_cost < dp[i + length]:
                            dp[i + length] = dp[i] + total_cost
                            
        return dp[n] if dp[n] != float('inf') else -1