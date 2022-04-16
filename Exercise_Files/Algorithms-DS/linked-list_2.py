class Node:
     
    def __init__(self, data):    
        self.data = data 
        self.next = None 
    
    def __str__(self):
        return " {} ->".format(self.data)

class MyLinkedList:

    def __init__(self):
        self.head = None 
      
    def get(self, index: int) -> int:
        temp = self.head
        i = 0 
        while temp is not None:
            if i == index:
               return temp.data  
            i += 1   
            temp = temp.next    
        return -1     

    def addAtHead(self, val: int) -> None:
        temp = Node(val)
        temp.next = self.head 
        self.head = temp
    
    def addAtTail(self, val: int) -> None:
        new_node = Node(val)
        if self.head is None:
           self.head = new_node
           return
        else:    
           temp = self.head 
        while temp.next is not None:
            temp = temp.next
        temp.next = new_node    

    def addAtIndex(self, index: int, val: int) -> None:
        new_node = Node(val)
        temp = self.head
        prev_node = temp 
        
        if index == 0:
            new_node.next = temp
            self.head = new_node
            return     

        i = 0 
        while temp is not None:
            if i == index:
                break
            i += 1
            prev_node = temp 
            temp = temp.next    

        if index <= i:     
           prev_node.next = new_node
           new_node.next = temp    
            
        return        

    def deleteAtIndex(self, index: int) -> None:
        temp = self.head
        prev_node = temp

        if index == 0 and temp is not None:
           self.head = temp.next
           return

        i = 0
        while temp is not None:
                if i == index:
                    prev_node.next = temp.next
                    break  
                i += 1
                prev_node = temp 
                temp = temp.next



    def print_list(self) -> None:
        ll = ""
        temp = self.head 
        ll = " HEAD ->"
        while temp is not None:
              ll += " {} -> ".format(temp.data) 
              temp = temp.next  
        ll += " TAIL"
        print(ll)
        
        


# Your MyLinkedList object will be instantiated and called as such:
obj = MyLinkedList()


obj.addAtIndex(1,0)
print(obj.get(0))
obj.print_list() 



print("\n\n")





#obj.addAtHead(1)
#obj.addAtIndex(0,10)
#obj.print_list() 
#obj.addAtIndex(0,20)
#obj.addAtIndex(1,20)
#obj.print_list() 
#print(obj.get(0))

#obj.deleteAtIndex(0)
#print(obj.get(0))
#obj.print_list() 


'''
    def get(self, index: int) -> int:  
        asdsa
        
    def addAtTail(self, val: int) -> None:
        

    def addAtIndex(self, index: int, val: int) -> None:
        

    def deleteAtIndex(self, index: int) -> None:


'''