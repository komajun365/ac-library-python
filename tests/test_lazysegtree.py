from atcoder import LazySegTree
import pytest


def op_ss(a, b):
    return max(a, b)


def op_ts(a, b):
    return a+b


def op_tt(a, b):
    return a+b


def e_s():
    return -1_000_000_000


def e_t():
    return 0


def starry_seg(n=0, v=[]):
    if v:
        s = LazySegTree(op=op_ss,
                        e=e_s,
                        mapping=op_ts,
                        composition=op_tt,
                        id=e_t,
                        v=v)
    else:
        s = LazySegTree(op=op_ss,
                        e=e_s,
                        mapping=op_ts,
                        composition=op_tt,
                        id=e_t,
                        n=n)
    return s


def test_lazysegtree_zero():
    s = starry_seg(n=0)
    assert s.all_prod() == -1_000_000_000
    s = starry_seg()
    assert s.all_prod() == -1_000_000_000
    s = starry_seg(n=10)
    assert s.all_prod() == -1_000_000_000


def test_lazysegtree_assign():
    seg0 = starry_seg()
    seg0 = starry_seg(n=10)


def test_lazysegtree_invalid1():
    with pytest.raises(AssertionError) as e:
        s = starry_seg(n=-1)


@pytest.mark.parametrize("p", [
    -1, 10
])
def test_lazysegtree_invalid2(p):
    s = starry_seg(n=10)
    with pytest.raises(AssertionError) as e:
        s.get(p)


@pytest.mark.parametrize(("l", "r"), [
    (-1, -1),
    (3, 2),
    (0, 11),
    (-1, 11)
])
def test_lazysegtree_invalid3(l, r):
    s = starry_seg(n=10)
    with pytest.raises(AssertionError) as e:
        s.prod(l, r)


def test_lazysegtree_naiveprod():
    for n in range(51):
        seg = starry_seg(n=n)
        p = [0] * n
        for i in range(n):
            p[i] = (i * i + 100) % 31
            seg.set(i, p[i])
        for l in range(n+1):
            for r in range(l, n+1):
                e = -1_000_000_000
                for i in range(l, r):
                    e = max(e, p[i])
                assert e == seg.prod(l, r)


def test_lazysegtree_usage():
    v = [0] * 10
    seg = starry_seg(v=v)
    assert 0 == seg.all_prod()
    seg.apply_lr(0, 3, 5)
    assert 5 == seg.all_prod()
    seg.apply(2, -10)
    assert -5 == seg.prod(2, 3)
    assert 0 == seg.prod(2, 4)
