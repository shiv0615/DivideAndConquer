import numpy as np

def SwapElem(arr, swap_index, elem_index):
    swap_elem       = arr[swap_index]
    arr[swap_index] = arr[elem_index]
    arr[elem_index] = swap_elem

def quick_sort(a, l_index, r_index, pivot_choice):
    if l_index >= r_index: return
    p_elem, p_index = ChoosePivot(a, l_index, r_index, pivot_choice)
    SwapElem(a, l_index, p_index)
    part_indx_left, part_indx_right  = Partition(a, l_index, r_index)
    quick_sort(a, l_index, part_indx_left, pivot_choice)
    quick_sort(a, part_indx_right, r_index, pivot_choice)

def Partition(a, l_index, r_index):
    global m_compare
    m_compare = m_compare + r_index - l_index
    i      = l_index + 1
    p_elem = a[l_index]
    for j in range(l_index+1, r_index+1):
        if a[j] < p_elem:
            SwapElem(a, i, j)
            i         = i+1
    equals = 0
    for j in range(i, r_index + 1):
        if a[j] == p_elem:
            SwapElem(a, i+equals, j)
            equals = equals + 1
    SwapElem(a, i-1, l_index)
    return i - 2, i+equals

def ChoosePivot(a, l_index, r_index, pivot_choice='first'):
    if pivot_choice == 'first' or \
       pivot_choice == 'left':
        return a[l_index], l_index
    elif pivot_choice == 'last' or \
         pivot_choice == 'right':
        return a[r_index], r_index
    elif pivot_choice == 'middle':
        n = len(a[l_index:r_index+1])
        if n%2 == 0:
            indx = l_index + int(n/2) - 1
        else:
            indx = l_index + int((n+1)/2) - 1
        if ((a[indx]-a[l_index])*(a[r_index]-a[l_index])) <= 0:
            return a[l_index], l_index
        elif ((a[l_index]-a[indx])*(a[r_index]-a[indx])) <= 0:
            return a[indx], indx
        elif ((a[l_index]-a[r_index])*(a[indx]-a[r_index])) <= 0:
            return a[r_index], r_index
    else:
        np.randome.seed(120112)
        ranindx = np.random.randint(low=l_index,high=r_index)
        return a[ranindx], ranindx

if __name__ =='__main__':
    a = [8, 5, 6,7,9,34,356,56,8, 25]
    filename = r''
    a = np.loadtxt(filename, delimiter="\n", ).tolist()
    print('Pre Sorder List: ', a)
    pivot_choice = 'middle'
    m_compare = 0
    quick_sort(a, l_index = 0, r_index=len(a)-1, pivot_choice=pivot_choice)
    print('Sorder List: ', a)
    print('# Comparisons: ', m_compare)
    print('Pivot Choice: ', pivot_choice.capitalize())
