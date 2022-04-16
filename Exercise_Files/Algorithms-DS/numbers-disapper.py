 

import time 
nums = [4,3,2,7,8,2,3,1]
 
curr_val = 0
n = len(nums)
ret_list = []
j=1

for i in range(n):
    curr_val = nums[i] 
    print(curr_val,i+1,ret_list, nums)
    while curr_val != i+1:
        print("--->>>>", nums[curr_val-1],nums[i], nums, j )
        time.sleep(2.4)
        nums[curr_val-1], nums[i] = nums[i], nums[curr_val-1]
        curr_val = nums[i]
        j += 1
        if nums[i] == nums[curr_val-1]:
            ret_list.append(j)           
            break 
    
print(ret_list)        