arr = [3,3]

MAX1, MAX2, MAX3 = -999,-999,-999
for j in range(len(arr)):
   if arr[j] > MAX1:
    MAX3 = MAX2
    MAX2 = MAX1
    MAX1 = arr[j]
    print(MAX1, MAX2, MAX3)
   elif arr[j] > MAX2:
    MAX3 = MAX2
    MAX2 = arr[j]
   elif arr[j] > MAX3:
    MAX3 = arr[j]     

print(max(MAX1, MAX2, MAX3))   