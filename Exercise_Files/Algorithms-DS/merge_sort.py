def merge_sort(lst):
    """
    Merge sort function
    :param lst: lst of unsorted integers
    """
    n = len(lst)
    if ( n > 1 ):
        mid = n // 2
        left = lst[:mid]
        right = lst[mid:]
        merge_sort(left)
        merge_sort(right)
        return merge(lst, left, right)

def merge(lst, left, right):
        res = []
        i, j, k = 0,0,0
        while i < len(left) and j < len(right):
            if left[i] > right[j]:
                lst[k] = right[j]
                j += 1
                k += 1
            else:
                lst[k] = left[i]
                i += 1 
                k += 1    
        
        while i < len(left):
            lst[k] = left[i]
            i += 1
            k += 1 
            
        while j < len(right):
            lst[k] = right[j]
            j += 1
            k += 1   

        return lst           

# Driver code to test the above code
if __name__ == '__main__':

    lst = [3, 2, 1, 5, 4]
    print(merge_sort(lst))

    print("Sorted list is: ", lst)
