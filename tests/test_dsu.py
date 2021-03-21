from atcoder import DSU


def test_dsu_zero():
    uf = DSU(0)
    assert uf.groups() == []


def test_dsu_assign():
    uf = DSU(10)


def test_dsu_simple():
    uf = DSU(2)
    assert uf.same(0, 1) == False

    x = uf.merge(0, 1)
    assert x == uf.leader(0)
    assert x == uf.leader(1)
    assert uf.same(0, 1)
    assert 2 == uf.size(0)


def test_dsu_line():
    n = 500000
    uf = DSU(n)
    for i in range(n - 1):
        uf.merge(i, i + 1)
    assert n == uf.size(0)
    assert 1 == len(uf.groups())


def test_dsu_line_reverse():
    n = 500000
    uf = DSU(n)
    for i in reversed(range(n - 1)):
        uf.merge(i, i + 1)
    assert n == uf.size(0)
    assert 1 == len(uf.groups())
