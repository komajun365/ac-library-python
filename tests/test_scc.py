from atcoder import Scc
import pytest


def test_empty():
    graph0 = Scc()
    graph1 = Scc(0)
    assert [] == graph0.scc()
    assert [] == graph1.scc()


def test_assign():
    graph = Scc(10)
    assert isinstance(graph, Scc)


def test_simple():
    graph = Scc(2)
    graph.add_edge(0, 1)
    graph.add_edge(1, 0)
    scc = graph.scc()
    assert len(scc) == 1


def test_selfloop():
    graph = Scc(2)
    graph.add_edge(0, 0)
    graph.add_edge(0, 0)
    graph.add_edge(1, 1)
    scc = graph.scc()
    assert len(scc) == 2


def test_invalid():
    graph = Scc(2)
    with pytest.raises(AssertionError) as e:
        graph.add_edge(0, 10)
