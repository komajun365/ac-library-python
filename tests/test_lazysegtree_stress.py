from atcoder import LazySegTree
import random
from tests.utils.random import randpair


class TimeManager:
    def __init__(self, n):
        self.v = [-1] * n
    
    def action(self, l, r, time):
        for i in range(l, r):
            self.v[i] = time
    
    def prod(self, l, r):
        res = -1
        for i in range(l, r):
            res = max(res, self.v[i])
        return res


class S:
    def __init__(self, l=0, r=0, time=0):
        self.l = l
        self.r = r
        self.time = time


class T:
    def __init__(self, new_time):
        self.new_time = new_time


def op_ss(l: S, r: S):
    if l.l == -1:
        return r
    if r.l == -1:
        return l
    assert l.r == r.l
    return S(l.l, r.r, max(l.time, r.time))


def op_ts(l: T, r: S):
    if l.new_time == -1:
        return r
    assert r.time < l.new_time
    return S(r.l, r.r, l.new_time)


def op_tt(l: T, r: T):
    if l.new_time == -1:
        return r
    if r.new_time == -1:
        return l
    assert l.new_time > r.new_time
    return l


def e_s():
    return S(-1, -1, -1)


def e_t():
    return T(-1)


def seg(n=0, v=[]):
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


def test_lazysegtree_naivetest_stress():
    for n in range(1, 31):
        for ph in range(0, 10):
            seg0 = seg(n=n)
            tm = TimeManager(n)
            for i in range(n):
                seg0.set(i, S(i, i+1, -1))
            now = 0
            for q in range(3000):
                ty = random.randint(0, 3)
                l, r = randpair(0, n)
                if ty == 0:
                    res = seg0.prod(l, r)
                    assert l == res.l
                    assert r == res.r
                    assert tm.prod(l, r) == res.time
                elif ty == 1:
                    res = seg0.get(l)
                    assert l == res.l
                    assert l + 1 == res.r
                    assert tm.prod(l, l + 1) == res.time
                elif ty == 2:
                    now += 1
                    seg0.apply_lr(l, r, T(now))
                    tm.action(l, r, now)
                elif ty == 3:
                    now += 1
                    seg0.apply(l, T(now))
                    tm.action(l, l + 1, now)
                else:
                    assert False


def test_lazysegtree_maxright_stress():
    for n in range(1, 31):
        for ph in range(0, 10):
            seg0 = seg(n=n)
            tm = TimeManager(n)
            for i in range(n):
                seg0.set(i, S(i, i+1, -1))
            now = 0
            for q in range(1000):
                ty = random.randint(0, 2)
                l, r = randpair(0, n)
                if ty == 0:
                    def maxright_g(s):
                        if s.l == -1:
                            return True
                        assert s.l == l
                        assert s.time == tm.prod(l, s.r)
                        return s.r <= r
                    assert r == seg0.max_right(l, maxright_g)
                else:
                    now += 1
                    seg0.apply_lr(l, r, T(now))
                    tm.action(l, r, now)


def test_lazysegtree_minleft_stress():
    for n in range(1, 31):
        for ph in range(0, 10):
            seg0 = seg(n=n)
            tm = TimeManager(n)
            for i in range(n):
                seg0.set(i, S(i, i+1, -1))
            now = 0
            for q in range(1000):
                ty = random.randint(0,2)
                l, r = randpair(0, n)
                if ty == 0:
                    def minleft_g(s):
                        if s.l == -1:
                            return True
                        assert s.r == r
                        assert s.time == tm.prod(s.l, r)
                        return l <= s.l
                    assert l == seg0.min_left(r, minleft_g)
                else:
                    now += 1
                    seg0.apply_lr(l, r, T(now))
                    tm.action(l, r, now)
