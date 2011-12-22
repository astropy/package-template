def fib(n):
    """Returns the Fibonacci series up to n."""
    a, b = 0, 1
    c = []
    while b < n:
        c.append(b)
        a, b = b, a + b
    return c