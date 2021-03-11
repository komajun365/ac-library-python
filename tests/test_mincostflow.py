from atcoder import MinCostFlow
from atcoder import MaxFlow
import pytest
from tests.utils.random import randpair
from random import randint


def test_zero():
    g1 = MinCostFlow()
    g2 = MinCostFlow(0)

# def edge_eq(expect, actual):
#     assert expect == actual


def test_simple():
    g = MinCostFlow(4)
    g.add_edge(0, 1, 1, 1)
    g.add_edge(0, 2, 1, 1)
    g.add_edge(1, 3, 1, 1)
    g.add_edge(2, 3, 1, 1)
    g.add_edge(1, 2, 1, 1)
    expect = [[0, 0], [2, 4]]
    assert expect == g.slope(0, 3, 10)

    assert g.get_edge(0) == [0, 1, 1, 1, 1]
    assert g.get_edge(1) == [0, 2, 1, 1, 1]
    assert g.get_edge(2) == [1, 3, 1, 1, 1]
    assert g.get_edge(3) == [2, 3, 1, 1, 1]
    assert g.get_edge(4) == [1, 2, 1, 0, 1]


def test_usage():
    g = MinCostFlow(2)
    g.add_edge(0, 1, 1, 2)
    assert [1, 2] == g.flow(0, 1)

    g = MinCostFlow(2)
    g.add_edge(0, 1, 1, 2)
    assert [[0, 0], [1, 2]] == g.slope(0, 1)


@pytest.mark.parametrize("p", [
    [-1, 3], [3, 3]
])
def test_assign(p):
    g = MinCostFlow()
    s, t = p
    with pytest.raises(AssertionError) as e:
        g.slope(s, t)


# https://github.com/atcoder/ac-library/issues/1
def test_selfloop():
    g = MinCostFlow(3)
    assert 0 == g.add_edge(0, 0, 100, 123)
    assert [0, 0, 100, 0, 123] == g.get_edge(0)


def test_samecostpaths():
    g = MinCostFlow(3)
    assert 0 == g.add_edge(0, 1, 1, 1)
    assert 1 == g.add_edge(1, 2, 1, 0)
    assert 2 == g.add_edge(0, 2, 2, 1)
    assert [[0, 0], [3, 3]] == g.slope(0, 2)


@pytest.mark.parametrize("p", [
    [0, 0, -1, 0], [0, 0, 0, -1]
])
def test_invalid(p):
    g = MinCostFlow(2)
    # https://github.com/atcoder/ac-library/issues/51
    with pytest.raises(AssertionError) as e:
        g.add_edge(*p)


def test_stress():
    for phase in range(1000):
        n = randint(2, 20)
        m = randint(1, 100)
        s, t = randpair(0, n-1)
        if randint(0, 1):
            s, t = t, s
        
        g_mf = MaxFlow(n)
        g = MinCostFlow(n)
        for i in range(m):
            u = randint(0, n-1)
            v = randint(0, n-1)
            cap = randint(0, 10)
            cost = randint(0, 10000)
            g.add_edge(u, v, cap, cost)
            g_mf.add_edge(u, v, cap)
        
        flow, cost = g.flow(s, t)
        assert g_mf.flow(s, t) == flow

        cost2 = 0
        v_cap = [0] * n
        for from_, to, _, flow_e, cost_e in g.edges():
            v_cap[from_] -= flow_e
            v_cap[to] += flow_e
            cost2 += flow_e * cost_e
        assert cost == cost2

        for i in range(n):
            if i == s:
                assert -flow == v_cap[i]
            elif i == t:
                assert flow == v_cap[i]
            else:
                assert 0 == v_cap[i]
        
        # check: there is no negative-cycle
        dist = [0] * n
        while True:
            update = False
            for from_, to, cap, flow_e, cost_e in g.edges():
                if flow_e < cap:
                    ndist = dist[from_] + cost_e
                    if ndist < dist[to]:
                        update = True
                        dist[to] = ndist
                if flow_e:
                    ndist = dist[to] - cost_e
                    if ndist < dist[from_]:
                        update = True
                        dist[from_] = ndist
            if not update:
                break
