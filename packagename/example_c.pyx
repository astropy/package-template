def primes(int imax):
    """Returns prime numbers up to imax. This can only get up to 10000
    prime numbers."""
    cdef int n, k, i
    cdef int p[10001]
    result = []
    k = 0
    n = 2
    i = 0
    
    if imax>10000:
        imax = 10000
    while len(result) < imax:
        i = 0
        while i < k and n % p[i] != 0:
            i = i + 1
        if i == k:
            p[k] = n
            k = k + 1
            result.append(n)
            if k>10000:
                break
        n = n + 1
    return result