from atcoder import Convolution
from random import randint


NUMERIC_MAX_INT = 2**31 - 1


def conv_naive(a, b, mod):
    n = len(a)
    m = len(b)
    c = [0] * (n+m-1)
    for i in range(n):
        for j in range(m):
            c[i+j] += a[i] * b[j]
            c[i+j] %= mod
    
    return c


def test_convolution_empty():
    mod = 998244353
    conv = Convolution(mod)
    assert conv.convolution([], []) == []
    assert conv.convolution([], [1, 2]) == []
    assert conv.convolution([1, 2], []) == []
    assert conv.convolution([1], []) == []


def test_convolution_mid():
    mod = 998244353
    n = 1234
    m = 2345
    a = [randint(0, NUMERIC_MAX_INT) for i in range(n)]
    b = [randint(0, NUMERIC_MAX_INT) for i in range(m)]
    conv = Convolution(mod)
    assert conv_naive(a, b, mod) == conv.convolution(a, b)


def test_convolution_simplemod():
    mod1 = 998244353
    mod2 = 924844033
    conv = Convolution(mod1)
    a = [randint(0, NUMERIC_MAX_INT) for i in range(20)]
    b = [randint(0, NUMERIC_MAX_INT) for i in range(20)]
    assert conv_naive(a, b, mod1) == conv.convolution(a, b)

    conv = Convolution(mod2)
    a = [randint(0, NUMERIC_MAX_INT) for i in range(20)]
    b = [randint(0, NUMERIC_MAX_INT) for i in range(20)]
    assert conv_naive(a, b, mod2) == conv.convolution(a, b)


def test_convolution_simpleint():
    mod1 = 998244353
    mod2 = 924844033
    conv = Convolution(mod1)
    a = [randint(0, NUMERIC_MAX_INT) % mod1 for i in range(20)]
    b = [randint(0, NUMERIC_MAX_INT) % mod1 for i in range(20)]
    assert conv_naive(a, b, mod1) == conv.convolution(a, b)

    conv = Convolution(mod2)
    a = [randint(0, NUMERIC_MAX_INT) % mod2 for i in range(20)]
    b = [randint(0, NUMERIC_MAX_INT) % mod2 for i in range(20)]
    assert conv_naive(a, b, mod2) == conv.convolution(a, b)
