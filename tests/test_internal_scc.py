from atcoder import InternalScc
import pytest

def test_empty():
    graph0 = InternalScc()
    graph1 = InternalScc(0)
    assert len([]) == len(graph0.edges)
    assert len([]) == len(graph1.edges)

def test_assign():
    pass

def test_selfloop():
    pass

def test_invalid():
    pass