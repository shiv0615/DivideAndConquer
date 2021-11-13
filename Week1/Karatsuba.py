import numpy as np
import sys
EPSILLON = 1e-8

def karatsuba_multiply_integers(num1,num2):
    print(num1, num2)
    n1 = max(int(np.floor(np.log10(num1+EPSILLON))) + 1,1)
    n2 = max(int(np.floor(np.log10(num2+EPSILLON))) + 1,1)
    if n1*n2 == 1:
        return num1*num2
    else:
        n = max(n1,n2)
        n_by_2 = int(n / 2)
        n_by_2_prime = n - n_by_2
        print('num1 = %8d, num2 = %d, n_by_2 = %3d,  n_by_2_prime = %3d'%(num1, num2, n_by_2,n_by_2_prime))
        a = int(num1 / (10 ** n_by_2))
        b = int(num1 - a * (10 ** n_by_2))
        c = int(num2 / (10 ** n_by_2_prime))
        d = int(num2 - c * (10 ** n_by_2_prime))
        print('a = %8d, b = %8d, c = %8d, d = %8d'%(a,b,c,d))
        ac = karatsuba_multiply_integers(a, c)
        ad = karatsuba_multiply_integers(a, d)
        cb = karatsuba_multiply_integers(c, b)
        bd = karatsuba_multiply_integers(b, d)
        prod = 10**(n)*ac + (10 ** n_by_2*ad + 10**n_by_2_prime*cb) + bd
        return prod

def karatsuba_multiply_integers_as_strings(num1,num2):

    num1s = str(num1)
    num2s = str(num2)
    n1 = len(num1s)
    n2 = len(num2s)
    if n1*n2 == 1:
        return num1*num2
    else:
        n    = max(n1,n2)
        nby2 = n - int(n/2)
        offset = n%2
        num1s = num1s.rjust(n,'0')
        num2s = num2s.rjust(n,'0')
        a = int(num1s[:nby2])
        b = int(num1s[nby2:])
        c = int(num2s[:nby2])
        d = int(num2s[nby2:])
        print('num1 = %s, num2 = %s, n = %1d,  nby2 = %1d' % (num1s, num2s, n, nby2))
        print('a = %1d, b = %1d, c = %1d, d = %1d'%(a,b,c,d))
        ac = karatsuba_multiply_integers_as_strings(a, c)
        bd = karatsuba_multiply_integers_as_strings(b, d)
        ad_plus_bc = karatsuba_multiply_integers_as_strings(a+b, c+d) - ac - bd
        print('ac = %1d, bd = %1d, ad_plus_bc = %1d, n = %1d, nby2 = %1d' % (ac, bd, ad_plus_bc,n,nby2))
        prod = 10**(n-offset)*ac + 10**(nby2-offset)*ad_plus_bc + bd
        return prod

def main(a,b):
    # print('Multiplying two integers a = %8d and b = %8d of equal and even length using Karatsuba Method' % (a, b))
    prod = karatsuba_multiply_integers_as_strings(a, b)
    print('a,b, product, error: ', a, b, prod, prod - a*b)

if __name__ =='__main__':
    a = 3141592653589793238462643383279502884197169399375105820974944592
    b = 2718281828459045235360287471352662497757247093699959574966967627
    main(a,b)