def fact(n):
    if n in [0,1]:  # noqa
        return 1
    return n * fact(n - 1)
