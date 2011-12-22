def fib(n):
    """Returns the Fibonacci series up to n."""
    a, b = 0, 1
    c = []
    while b < n:
        c.append(b)
        a, b = b, a + b
    return c

def do_fib(n, usecython=False):
    if usecython:
        from .example_c import fib as cfib

        print 'Using cython-based fib'

        return cfib(n)
    else:
        print 'Using pure python fib'

        return fib(n)


def main(args=None):
    from astropy.utils.compat import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--use-cython', dest='cy', action='store_true',
                        help='Use the Cython-based Fibonacci generator.')
    parser.add_argument('n', metavar='N', type=int,
                        help='Run Fibonacci series up to this number.')

    res = parser.parse_args(args)

    fib = do_fib(res.n, res.cy)
    print fib
