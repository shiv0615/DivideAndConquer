import random

import numpy  as np

def recursive_split(a):
    n = len(a)
    sorted_array = []
    if n > 1:
        left_array = a[:int(n/2)]
        right_array=a[int(n/2):]
        recursive_split(left_array)
        recursive_split(right_array)
        print(left_array)
        print(right_array)
        i = 0
        j = 0
        k = 0
        while i < len(left_array) and j < len(right_array):
            if left_array[i] < right_array[j]:
                sorted_array[k] = left_array[i]
                i+=1
            else:
                sorted_array[k] = right_array[i]
                j += 1
            k+=1
        return sorted_array

def main(n):
    a = [random.randint(1,10) for i in range(n)]
    print('Input List: ', a)
    sorted_a = recursive_split(a)
    print('sorted List: ',sorted_a)

if __name__ =='__main__':
    main(n=8)
