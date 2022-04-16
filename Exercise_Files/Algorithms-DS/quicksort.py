

def quick_sort(unsorted_list):
    sorted_list = []
    
    if(len(unsorted_list)<=1):
        return unsorted_list

    left = []
    right = []
    pivot = unsorted_list[0]

    for i in unsorted_list[1:]:
        if ( i > pivot ):
            right.append(i)
        else: 
            left.append(i)    
    return quick_sort(left) + [pivot]  + quick_sort(right) 


sorted_list = quick_sort([17,3,1,33,12,1,45,19])
print(sorted_list)