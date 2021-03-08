from atcoder import SegTree
import pytest


class segtree_naive:
    def __init__(self, op, e, n=0):
        self._n = n
        self._d = [e() for _ in range(n)]
        self._op = op
        self._e = e

    def set(self, p, x):
        self._d[p] = x

    def get(self, p):
        return d[p]

    def prod(self, l, r):
        total = self._e()
        for i in range(l,r):
            total = self._op(total, self._d[i])
        return total

    def all_prod(self):
        return self.prod(0, self._n)

    def max_right(self, l, f):
        total = self._e()
        assert f(total)
        for i in range(l, self._n):
            total = self._op(total, self._d[i])
            if not f(total):
                return i
        return self._n

    def min_left(self, r, f):
        total = self._e()
        assert f(total)
        for i in range(r-1, -1, -1):
            total = self._op(d[i], total)
            if not f(total):
                return i+1
        return 0


def op(a, b):
    assert a == '$' or b == '$' or a <= b
    if a == '$':
        return b
    if b == '$':
        return a
    return a+b


def e():
    return '$'


def seg(n=None, v=[]):
    if n is None:
        return SegTree(op, e, v=v)
    return SegTree(op, e, n=n)


def seg_naive(n):
    return segtree_naive(op, e, n)


def test_zero():
    s = seg(0)
    assert '$' == s.all_prod()

    s = seg()
    assert '$' == s.all_prod()


def test_invalid():
    with pytest.raises(AssertionError) as e:
        s = seg(n=-1)


@pytest.mark.parametrize("p", [
    -1, 10
])
def test_invalid_get(p):
    s = seg(10)
    with pytest.raises(AssertionError) as e:
        s.get(p)


@pytest.mark.parametrize("p", [
    [-1, -1],
    [3, 2],
    [0, 11],
    [-1, 11],
])
def test_invalid_prod(p):
    s = seg(10)
    with pytest.raises(AssertionError) as e:
        s.prod(*p)

@pytest.mark.parametrize("p", [
    [11, True],
    [0, False]
])
def test_invalid_maxright(p):
    s = seg(10)
    num, b = p
    with pytest.raises(AssertionError) as e:
        s.max_right(num, lambda x: b)


@pytest.mark.parametrize("p", [
    [-1, True],
    ])
def test_invalid_minleft(p):
    s = seg(10)
    num, b = p
    with pytest.raises(AssertionError) as e:
        s.min_left(num, lambda x: b)


def test_one():
    s = seg(1)
    assert '$' == s.all_prod()
    assert '$' == s.get(0)
    assert '$' == s.prod(0, 1)
    s.set(0, 'dummy')
    assert 'dummy' == s.get(0)
    assert '$' == s.prod(0, 0)
    assert 'dummy' == s.prod(0, 1)
    assert '$' == s.prod(1, 1)


def test_compare_naive():
    y = ''
    
    def leq_y(x):
        return len(x) <= len(y)

    for n in range(30):
        seg0 = seg_naive(n=n)
        seg1 = seg(n=n)
        for i in range(n):
            s = ''
            s += chr(ord('a') + i)
            seg0.set(i, s)
            seg1.set(i, s)
        
        for l in range(n+1):
            for r in range(l, n+1):
                assert seg0.prod(l, r) == seg1.prod(l, r)
        
        for l in range(n+1):
            for r in range(l, n+1):
                y = seg1.prod(l, r)
                assert seg0.max_right(l, leq_y) == seg1.max_right(l, leq_y)
                assert seg0.max_right(l, leq_y) == \
                       seg1.max_right(l, lambda x: len(x) <= len(y))


def test_assign():
    seg0 = seg()
    seg0 = seg(10)
