from atcoder import TwoSAT
import random


def test_empty():
    ts0 = TwoSAT()
    assert ts0.satisfiable()
    assert [] == ts0.answer()
    ts1 = TwoSAT(0)
    assert ts1.satisfiable()
    assert [] == ts1.answer()


def test_one():
    ts = TwoSAT(1)
    ts.add_clause(0, True, 0, True)
    ts.add_clause(0, False, 0, False)
    assert not ts.satisfiable()

    ts = TwoSAT(1)
    ts.add_clause(0, True, 0, True)
    assert ts.satisfiable()
    assert [True] == ts.answer()

    ts = TwoSAT(1)
    ts.add_clause(0, False, 0, False)
    assert ts.satisfiable()
    assert [False] == ts.answer()


def test_assign():
    ts = TwoSAT()
    ts = TwoSAT(10)


def test_stressOK():
    for phase in range(10000):
        n = random.randint(1, 20)
        m = random.randint(1, 100)
        expect = [random.randint(0,1) for _ in range(n)]
        ts = TwoSAT(n)
        xs = [0] * m
        ys = [0] * m
        types = [0] * m
        for i in range(m):
            x = random.randint(0, n-1)
            y = random.randint(0, n-1)
            type_ = random.randint(0, 2)
            xs[i] = x
            ys[i] = y
            types[i] = type_
            if type_ == 0:
                ts.add_clause(x, expect[x], y, expect[y])
            elif type_ == 1:
                ts.add_clause(x, 1 - expect[x], y, expect[y])
            else:
                ts.add_clause(x, expect[x], y, 1 - expect[y])
        assert ts.satisfiable()
        actual = ts.answer()
        for i in range(m):
            x, y, type_ = xs[i], ys[i], types[i]
            if type_ == 0:
                assert actual[x] == expect[x] or actual[y] == expect[y]
            elif type_ == 1:
                assert actual[x] != expect[x] or actual[y] == expect[y]
            else:
                assert actual[x] == expect[x] or actual[y] != expect[y]
