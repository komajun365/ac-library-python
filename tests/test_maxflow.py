from atcoder import MaxFlow
import pytest
import random
from tests.utils.random import randpair


def test_maxflow_zero():
    g1 = MaxFlow()
    g2 = MaxFlow(0)
    g1, g2


def test_maxflow_assign():
    g = MaxFlow()
    g = MaxFlow(10)
    g

# def edge_eq(expect, actual):
#     assert expect == actual


def test_maxflow_simple():
    g = MaxFlow(4)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 2, 1)
    assert 2 == g.add_edge(1, 3, 1)
    assert 3 == g.add_edge(2, 3, 1)
    assert 4 == g.add_edge(1, 2, 1)
    assert 2 == g.flow(0, 3)

    assert g.get_edge(0) == [0, 1, 1, 1]
    assert g.get_edge(1) == [0, 2, 1, 1]
    assert g.get_edge(2) == [1, 3, 1, 1]
    assert g.get_edge(3) == [2, 3, 1, 1]
    assert g.get_edge(4) == [1, 2, 1, 0]

    assert g.min_cut(0) == [True, False, False, False]


def test_maxflow_not_simple():
    g = MaxFlow(2)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 1, 2)
    assert 2 == g.add_edge(0, 1, 3)
    assert 3 == g.add_edge(0, 1, 4)
    assert 4 == g.add_edge(0, 1, 5)
    assert 5 == g.add_edge(0, 0, 6)
    assert 6 == g.add_edge(1, 1, 7)
    assert 15 == g.flow(0, 1)

    assert g.get_edge(0) == [0, 1, 1, 1]
    assert g.get_edge(1) == [0, 1, 2, 2]
    assert g.get_edge(2) == [0, 1, 3, 3]
    assert g.get_edge(3) == [0, 1, 4, 4]
    assert g.get_edge(4) == [0, 1, 5, 5]

    assert g.min_cut(0) == [True, False]


def test_maxflow_cut():
    g = MaxFlow(3)
    assert 0 == g.add_edge(0, 1, 2)
    assert 1 == g.add_edge(1, 2, 1)
    assert 1 == g.flow(0, 2)

    assert g.get_edge(0) == [0, 1, 2, 1]
    assert g.get_edge(1) == [1, 2, 1, 1]

    assert g.min_cut(0) == [True, True, False]


def test_maxflow_twice():
    g = MaxFlow(3)
    assert 0 == g.add_edge(0, 1, 1)
    assert 1 == g.add_edge(0, 2, 1)
    assert 2 == g.add_edge(1, 2, 1)
    assert 2 == g.flow(0, 2)

    assert g.get_edge(0) == [0, 1, 1, 1]
    assert g.get_edge(1) == [0, 2, 1, 1]
    assert g.get_edge(2) == [1, 2, 1, 1]

    g.change_edge(0, 100, 10)
    assert g.get_edge(0) == [0, 1, 100, 10]

    assert 0 == g.flow(0, 2)
    assert 90 == g.flow(0, 1)

    assert g.get_edge(0) == [0, 1, 100, 100]
    assert g.get_edge(1) == [0, 2, 1, 1]
    assert g.get_edge(2) == [1, 2, 1, 1]

    assert 2 == g.flow(2, 0)

    assert g.get_edge(0) == [0, 1, 100, 99]
    assert g.get_edge(1) == [0, 2, 1, 0]
    assert g.get_edge(2) == [1, 2, 1, 0]


def test_maxflow_bound():
    inf = 9_223_372_036_854_775_807
    g = MaxFlow(3)
    assert 0 == g.add_edge(0, 1, inf)
    assert 1 == g.add_edge(1, 0, inf)
    assert 2 == g.add_edge(0, 2, inf)
    assert inf == g.flow(0, 2)

    assert g.get_edge(0) == [0, 1, inf, 0]
    assert g.get_edge(1) == [1, 0, inf, 0]
    assert g.get_edge(2) == [0, 2, inf, inf]


# def test_maxflow_bounduint():
# 省略


def test_maxflow_selfloop():
    g = MaxFlow(3)
    assert 0 == g.add_edge(0, 0, 100)
    assert g.get_edge(0) == [0, 0, 100, 0]


@pytest.mark.parametrize("args", [
    [0, 0],
    [0, 0, 0]
])
def test_maxflow_invalid(args):
    with pytest.raises(AssertionError) as e:
        g = MaxFlow(3)
        g.flow(*args)


def test_maxflow_stress():
    for phase in range(10000):
        n = random.randint(2, 20)
        m = random.randint(1, 100)
        s, t = randpair(0, n-1)
        if random.randint(0, 1):
            s, t = t, s

        g = MaxFlow(n)
        for i in range(m):
            u = random.randint(0, n-1)
            v = random.randint(0, n-1)
            c = random.randint(0, 10000)
            g.add_edge(u, v, c)

        flow = g.flow(s, t)
        dual = 0
        cut = g.min_cut(s)
        v_flow = [0] * n
        for e_from, e_to, e_cap, e_flow in g.edges():
            v_flow[e_from] -= e_flow
            v_flow[e_to] += e_flow
            if cut[e_from] and (not cut[e_to]):
                dual += e_cap
        assert flow == dual
        assert flow * -1 == v_flow[s]
        assert flow == v_flow[t]
        for i in range(n):
            if(i == s) or (i == t):
                continue
            assert 0 == v_flow[i]
