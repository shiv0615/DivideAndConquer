import numpy as np
import sys
EPSILLON = 1e-8

def FindCrossInversion(n, al, ar):
    i = 0
    j = 0
    d = []
    pairs = 0
    for k in range(n):
        if(i < len(al) and j < len(ar)):
            if al[i] <= ar[j]:
                d.append(al[i])
                i = i + 1
            else:
                d.append(ar[j])
                pairs = pairs + (len(al) - i)
                j = j + 1
        if i == len(al):
            d = d + ar[j:]
            break
        elif j == len(ar):
            d = d + al[i:]
            break
    return d, pairs

def FindInversion(a):
    n = len(a)
    if n == 1:
        return a, 0
    elif n == 2:
        if a[0] < a[1]: return a, 0
        else: return [a[1],a[0]], 1
    else:
        nleft  = int(np.floor(n/2))
        al, pairsl = FindInversion(a[:nleft])
        ar, pairsr = FindInversion(a[nleft:])
        ac, pairsc = FindCrossInversion(n, al, ar)
        pairs = pairsl + pairsr + pairsc
        return ac, pairs

if __name__ =='__main__':
    a = [1,3,5,2,4,6,9,12,10,8,11]
    filename = r''
    a1 = np.loadtxt(filename, delimiter="\n",).tolist()
    a  = [int(elem) for elem in a1]
    sorted_a, pairs = FindInversion(a)
    print('Input  List: ', a[0:100])
    print('Output List: ', sorted_a)
    print('Inversion Pairs: ', pairs)




