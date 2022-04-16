

def selection_sort(unsorted_list):
    sorted_list = []
    while len(unsorted_list) > 0:
          least_value_pos = find_least_value(unsorted_list)
          sorted_list.append(unsorted_list.pop(least_value_pos))
    print(sorted_list)
    return sorted_list


def find_least_value(arr):
    pos = 0
    for i in range(len(arr)-1):
        if ( arr[pos] > arr[i+1] ):
           pos = i+1  
    return pos


def containsDuplicate(List):
        di = {}
        for i in List:
            if i not in di:
               di[i] = 1
            elif di[i] >= 1:
               print(di[i],i) 
               di[i] += 1
               return 1 

        print(di)        
        return 0

print(containsDuplicate([17,3,1,33,12,1,45,19,1]))

#selection_sort([17,3,1,33,12,1,45,19])