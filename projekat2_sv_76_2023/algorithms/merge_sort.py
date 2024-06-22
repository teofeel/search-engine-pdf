#def merge(arr, l, m, r):
#    n1 = m - l + 1
#    n2 = r - m
# 
#    L = [0] * (n1)
#    R = [0] * (n2)
# 
#    for i in range(0, n1):
#        L[i] = arr[l + i]
# 
#    for j in range(0, n2):
#        R[j] = arr[m + 1 + j]
# 
#    i = 0    
#    j = 0     
#    k = l     
# 
#    while i < n1 and j < n2:
#        if L[i]['rang'] <= R[j]['rang']:
#            arr[k] = L[i]
#            i += 1
#        else:
#            arr[k] = R[j]
#            j += 1
#        k += 1
# 
#    while i < n1:
#        arr[k] = L[i]
#        i += 1
#        k += 1
# 
#    while j < n2:
#        arr[k] = R[j]
#        j += 1
#        k += 1
# 
# 
# 
#def sort(arr, l, r):
#    if l < r:
#        m = l+(r-l)//2
# 
#        sort(arr, l, m)
#        sort(arr, m+1, r)
#        merge(arr, l, m, r)

def sort(arr):
    if len(arr) <= 1:
        return 
    
    mid = len(arr) // 2
    
    left_half = arr[:mid]
    right_half = arr[mid:]

    sort(left_half)
    sort(right_half)

    i = j = k = 0

    while i < len(left_half) and j < len(right_half):
        if left_half[i]['rang'] > right_half[j]['rang'] :
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1

    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1

    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1