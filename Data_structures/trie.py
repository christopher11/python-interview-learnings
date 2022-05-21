class TrieNode:
    def __init__(self, char=''):
        self.children = [None] * 26
        self.char = char
        self.end_word = False

    def __str__(self):   
        return f"{self.children}, {self.char}, {self.end_word}"

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def get_index(self, letter):
        return ord(letter) - ord('a')    

    def insert(self, key):
        current = self.root
        key = key.lower()

        for letter in key:
            
            index = self.get_index(letter)
            if current.children[index] == None:
               current.children[index] = TrieNode(letter) 
            
            current = current.children[index] 
            #print(current)
    
        current.end_word = True
         
        return 
         
    def search(self, key):

        current = self.root

        for letter in key:
            index = self.get_index(letter)
            if current is None or current.children[index] == None:
               return False

            current = current.children[index]

        if current.end_word:
             return True   

        return False 
        

t = Trie()

words = ["there", "their", "the", "amd", "bc"]

for word in words:
    t.insert(word)
    print("\n", t.root)



print(t)


print(t.search("the"), t.search("asdsadasd"), t.search("theirr"), t.search("amd"))






