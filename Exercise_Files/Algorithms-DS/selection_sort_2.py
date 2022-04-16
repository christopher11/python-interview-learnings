
def selection_rort(a):
    n = len(a) 
    for i in range(n):
        minindex = i 
        for j in range(i+1,n):
            if a[j] < a[minindex]:
               minindex = j
        a[i], a[minindex] = a[minindex], a[i]
    return a
        
arr = [2,3,1,2,4,19,1]
print(selection_rort(arr))
