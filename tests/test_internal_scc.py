from atcoder import InternalScc
import pytest


def test_empty():
    graph0 = InternalScc()
    graph1 = InternalScc(0)
    assert [] == graph0.scc()
    assert [] == graph1.scc()


def test_assign():
    graph = InternalScc(10)
    assert isinstance(graph, InternalScc)


def test_simple():
    graph = InternalScc(2)
    graph.add_edge(0, 1)
    graph.add_edge(1, 0)
    scc = graph.scc()
    assert len(scc) == 1


def test_selfloop():
    graph = InternalScc(2)
    graph.add_edge(0, 0)
    graph.add_edge(0, 0)
    graph.add_edge(1, 1)
    scc = graph.scc()
    assert len(scc) == 2
