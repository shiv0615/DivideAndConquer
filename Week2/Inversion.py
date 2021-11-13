import numpy as np
import sys
EPSILLON = 1e-8

def find_cross_inversion(n, al, ar):
    i = 0
    j = 0
    d = []
    pairs = []
    for k in range(n):
        # print(i, j, k)
        if(i < len(al) and j < len(ar)):
            if al[i] <= ar[j]:
                d.append(al[i])
                i = i + 1
            else:
                d.append(ar[j])
                pairs = pairs + [(al[e], ar[j]) for e in range(i, len(al))]
                j = j + 1
        if i == len(al):
            d = d + ar[j:]
            break
        elif j == len(ar):
            d = d + al[i:]
            break
    return d, pairs

def find_inversion(a):
    n = len(a)
    if n == 1:
        return a, None
    elif n == 2:
        if a[0] < a[1]: return a, None
        else: return [a[1],a[0]], [(a[0],a[1])]
    else:
        nleft  = int(np.floor(n/2))
        al, pairsl = find_inversion(a[:nleft])
        ar, pairsr = find_inversion(a[nleft:])
        ac, pairsc = find_cross_inversion(n, al, ar)
        pairs = []
        if pairsl is not None: pairs = pairs + pairsl
        if pairsr is not None: pairs = pairs + pairsr
        if pairsc is not None: pairs = pairs + pairsc
        return ac, pairs

if __name__ =='__main__':
    a = [1,3,5,2,4,6,9,12,10,8,11]

    filename = r'/Coursera/Algorithms_Part1/DivideAndConquer/Week2/iput.txt'
    a1 = np.loadtxt(filename, delimiter="\n",).tolist()
    a = [int(elem) for elem in a1]
    sorted_a, pairs = find_inversion(a)
    print('Input  List: ', a[0:100])
    print('Output List: ', sorted_a)
    print('Inversion Pairs: ', pairs)
    print('Number of Inversions: ', len(pairs))




