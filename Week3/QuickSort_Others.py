def partition(A, l, r):
    n = len(A)
    if n <= 1:
        return (A, 0)
    p = A[l]
    i = l + 1
    for j in range(l + 1, n):
        if A[j] < p:
            # swap A[i] and A[j]
            swap(A, i, j)
            i += 1
    # swap the pivot and the element before >p array
    swap(A, l, i - 1)

    # recursive call to partition
    # by splitting at pivot
    A1 = A[:i - 1]
    r1 = len(A1) - 1
    A2 = A[i:]
    r2 = len(A2) - 1
    B = partition(A1, 0, r1)
    C = partition(A2, 0, r2)
    count = B[1] + C[1] + n - 1
    return (B[0] + [A[i - 1]] + C[0], count)