from atcoder import LazySegTree
import random
from tests.utils.random import randpair


class TimeManager:
    def __init__(self, n):
        self.v = [-1] * n

    def action(self, left, right, time):
        for i in range(left, right):
            self.v[i] = time

    def prod(self, left, right):
        res = -1
        for i in range(left, right):
            res = max(res, self.v[i])
        return res


class S:
    def __init__(self, left=0, right=0, time=0):
        self.left = left
        self.right = right
        self.time = time


class T:
    def __init__(self, new_time):
        self.new_time = new_time


def op_ss(left: S, right: S):
    if left.left == -1:
        return right
    if right.left == -1:
        return left
    assert left.right == right.left
    return S(left.left, right.right, max(left.time, right.time))


def op_ts(left: T, right: S):
    if left.new_time == -1:
        return right
    assert right.time < left.new_time
    return S(right.left, right.right, left.new_time)


def op_tt(left: T, right: T):
    if left.new_time == -1:
        return right
    if right.new_time == -1:
        return left
    assert left.new_time > right.new_time
    return left


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
                left, right = randpair(0, n)
                if ty == 0:
                    res = seg0.prod(left, right)
                    assert left == res.left
                    assert right == res.right
                    assert tm.prod(left, right) == res.time
                elif ty == 1:
                    res = seg0.get(left)
                    assert left == res.left
                    assert left + 1 == res.right
                    assert tm.prod(left, left + 1) == res.time
                elif ty == 2:
                    now += 1
                    seg0.apply_lr(left, right, T(now))
                    tm.action(left, right, now)
                elif ty == 3:
                    now += 1
                    seg0.apply(left, T(now))
                    tm.action(left, left + 1, now)
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
                left, right = randpair(0, n)
                if ty == 0:
                    def maxright_g(s):
                        if s.left == -1:
                            return True
                        assert s.left == left
                        assert s.time == tm.prod(left, s.right)
                        return s.right <= right
                    assert right == seg0.max_right(left, maxright_g)
                else:
                    now += 1
                    seg0.apply_lr(left, right, T(now))
                    tm.action(left, right, now)


def test_lazysegtree_minleft_stress():
    for n in range(1, 31):
        for ph in range(0, 10):
            seg0 = seg(n=n)
            tm = TimeManager(n)
            for i in range(n):
                seg0.set(i, S(i, i+1, -1))
            now = 0
            for q in range(1000):
                ty = random.randint(0, 2)
                left, right = randpair(0, n)
                if ty == 0:
                    def minleft_g(s):
                        if s.left == -1:
                            return True
                        assert s.right == right
                        assert s.time == tm.prod(s.left, right)
                        return left <= s.left
                    assert left == seg0.min_left(right, minleft_g)
                else:
                    now += 1
                    seg0.apply_lr(left, right, T(now))
                    tm.action(left, right, now)
