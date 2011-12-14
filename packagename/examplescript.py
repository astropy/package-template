def fib(n):
    """Print the Fibonacci series up to n."""
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b


def do_fib(n, usecython=False):
    if usecython:
        from .example import fib

        print 'Using cython-based fib'

        fib(n)
    else:
        global fib

        print 'Using pure python fib'

        fib(n)


def main(args=None):
    from astropy.utils.compat import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--use-cython', dest='cy', action='store_true',
                        help='Use the Cython-based Fibonacci generator.')
    parser.add_argument('n', metavar='N', type=int,
                        help='Run Fibonacci series up to this number.')

    res = parser.parse_args(args)

    do_fib(res.n, res.cy)
