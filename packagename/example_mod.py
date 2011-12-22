def primes(imax):
    """Returns prime numbers up to imax.  This can only get up to 10000
    prime numbers."""
    p = range(10000)
    result = []
    k = 0
    n = 2
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
    
def do_primes(n, usecython=False):
    if usecython:
        from .example_c import primes as cprimes

        print 'Using cython-based primes'

        return cprimes(n)
    else:
        print 'Using pure python primes'

        return primes(n)


def main(args=None):
    from astropy.utils.compat import argparse
    from time import time

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--use-cython', dest='cy', action='store_true',
                        help='Use the Cython-based Prime number generator.')
    parser.add_argument('-t', '--timing', dest='time', action='store_true',
                        help='Time the Fibonacci generator.')
    parser.add_argument('-p', '--print', dest='prnt', action='store_true',
                        help='Print all of the Prime numbers.')
    parser.add_argument('n', metavar='N', type=int,
                        help='Get Prime numbers up to this number.')
    

    res = parser.parse_args(args)

    pre = time()
    prms = do_primes(res.n, res.cy)
    post = time()
    
    print 'Found',len(prms),'Prime numbers with',prms[-1],'as largest:'
    
    if res.time:
        print 'Running time:',post-pre,'s'
    if res.prnt:
        print prms
