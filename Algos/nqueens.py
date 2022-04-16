
'''    
        if s2 in self.generate_swap_strings(s1, s2):
           return True  
    
        if s1 in self.generate_swap_strings(s2, s1):
           return True
'''    
    
# Test 
            count = 0    
        for word in words:  
            word_count = 0
            used_cell = set()
            
            for row in range(m):
                for column in range(n):
                    count += 1
                    print(word, count)
                    if len(words) == len(res):
                       return res
                
                    if board[row][column] != word[0] or word in res:
                      continue
                    if dfs(row, column, word_count, word): 
                       res.append(word)