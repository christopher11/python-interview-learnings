class Node:
    def __init__(self,data):
        self.data = data
        self.next = None

    def __repr__(self):
        return "Node Data--> : %s"% self.data


class LinkedList:
    def __init__(self):
        self.head = None

    def __repr__(self):
        linkedlist = self.head 
        nodes = []
        while linkedlist is not None:
           nodes.append(linkedlist.data)
           linkedlist = linkedlist.next 
        nodes.append("None")
        return " -> ".join(nodes)  

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node.data
            node = node.next
    
    def add_first(self, node):
        node.next = self.head
        self.head = node

    def add_last(self, new_node):
        if self.head is None:
           self.head = new_node
           return
        node = self.head  
        while node is not None:
          if node.next is None:
             node.next = new_node
             break
          else: 
             node = node.next 

    def insert(self, target, new_node): 

        if self.head is None:
           raise Exception("List is empty")

        node = self.head 
        while node is not None:
            if node.data == target:
               temp  = node.next
               node.next = new_node
               new_node.next = temp
               break
            node = node.next
        return

    def remove(self, target): 
        if self.head.data == target:
           self.head = self.head.next
           return
        prev = self.head
        suc = prev.next
        while suc is not None:
            if suc.data == target:
               prev.next = suc.next
               break
            
            prev = suc
            suc = suc.next
        return

        


l1 = Node("a")
l2 = Node("b")
l3 = Node("c")
ll = LinkedList()
ll.head = l1
l1.next = l2 
l2.next = l3

l4 = Node("A")
l5 = Node("AA")
l6 = Node("JK")


ll.add_first(l4)
ll.add_last(l5)
print(ll)

ll.insert("b", l6)
print(ll)

ll.remove("A")
print(ll)



ll2 = LinkedList()
ll2.add_last(l5)
ll2.insert("AA", l6)
print(ll2)
ll2.remove("AA")
ll2.remove("JK")
print(ll2)