def duplicateZeros(arr):
        """
        Do not return anything, modify arr in-place instead.
        """
        print("", arr)
        possible_dups = 0
        length_ = len(arr) - 1

        # Find the number of zeros to be duplicated
        for left in range(length_ + 1):

            # Stop when left points beyond the last element in the original list
            # which would be part of the modified list
            if left > length_ - possible_dups:
                break

            # Count the zeros
            if arr[left] == 0:
                # Edge case: This zero can't be duplicated. We have no more space,
                # as left is pointing to the last element which could be included  
                if left == length_ - possible_dups:
                    arr[length_] = 0 # For this zero we just copy it without duplication.
                    length_ -= 1
                    break
                possible_dups += 1

        # Start backwards from the last element which would be part of new list.
        last = length_ - possible_dups

        print(possible_dups, "-->")
        # Copy zero twice, and non zero once.
        for i in range(last, -1, -1):
            print(i, arr)
            if arr[i] == 0:
                arr[i + possible_dups] = 0
                possible_dups -= 1
                arr[i + possible_dups] = 0
            else:
                arr[i + possible_dups] = arr[i]


        print("", arr)

print(duplicateZeros([0,4,1,0,0,8,0,0,3]))         




def merge(nums1, m, nums2, n):
        """
        Do not return anything, modify nums1 in-place instead.
        """
        
        i = j = k = 0
        while i < m or j < n:
            if nums1[i] > nums2[j]:
               nums1.insert(i, nums2[j])
            else:
               nums1.insert(i+1, nums2[j])
            nums1.pop()
            i += 2    
            j += 1


merge([1,2,3,0,0,0],)            


nput:
[0]
0
[1]
1



Output:
[0]
Expected:
[1]
Stdout:
0 1



[1]
1
[]
0


[0]
0
[1]
1