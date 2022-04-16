import random

class Node:
   def __init__(self, data):
       self.data = data
       self.right = None
       self.left = None
       self.parent = None

   def __repr__(self):
       print("{}<-{}-->{}".format(self.data,self.right, self.left))   

   def __str__(self):
       return "{}".format(self.data)

class BinarySearchTree:
    def __init__(self, data):
        self.root =  Node(data)

    def print(self):
        if self.root == None:
           print("Null Tree")
        else:
           print(self.traversal(self.root))

    
    def traversal(self, start):
        if start:
            
            self.traversal(start.right)
            print("{}-->".format(start.data), end=' ')
            self.traversal(start.left)

        return

    def iterative_traversal(self):
        curr = self.root  
        stack = []
        while curr is not None or not len(stack) == 0:

            if curr is not None:
               stack.append(curr)
               curr = curr.left  
            else:
               node = stack.pop()  
               print("{}-->".format(node.data), end=' ')
               curr = node.right
        return 

    def insert(self, data):
        node = Node(data)
        curr = self.root
        parent = None

        while curr:
              parent = curr
              if node.data < curr.data:
                 curr = curr.left
              else:
                 curr = curr.right   

        if node.data < parent.data:
           parent.left = node
        else:
           parent.right = node



    def insert_recursive(self, data, start):
        
        if start is None:
           return  Node(data)

        if start.data < data:
             start.left = self.insert_recursive(data, start.left)
        else:
             start.right = self.insert_recursive(data, start.right)

        return start

    def search(self, search_ele):
        curr = self.root
        while curr:
              if curr.data == search_ele:
                 return True 
              
              if curr.data < search_ele:
                 curr = curr.left
              else:  
                 curr = curr.right   
        return False

'''  
n1 = Node(1)
n2 = Node(2)
n3 = Node(3)

n1.left = Node(78)
n1.right = Node(99)

print(n1)
print("\n\n")
'''

iterative = BinarySearchTree(6)
recursive = BinarySearchTree(6)
#[23, 90, 45, 88, 2, 47, 6, 3, 79, 16] #
nodes = [1,2,3,4,5,6,7,8]  #[ random.randint(1,100) for x in range(10) ]
print("\n\nNodes: ", nodes)

for rand_num in nodes:

    iterative.insert(rand_num)
    recursive.insert_recursive(rand_num,recursive.root)



print("\nStart Traversal")
print("\n Iterative: ")
iterative.print()
print("\n Recursive: ")
recursive.print()

print("search status: ", recursive.search(99))

print("search status: ", recursive.search(6))
print("search status: ", recursive.search(67))

print("\n Iterative Traversal: ")
iterative.iterative_traversal()

print("\n  ")