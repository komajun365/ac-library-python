from atcoder import FenwickTree
import pytest

NUMERIC_MAX_INT = 2**31 - 1
NUMERIC_MIN_INT = -1 * 2**31

# int型以外およびオーバーフローを対象としたtestは実装しない


def test_enpty():
    fw = FenwickTree()
    assert 0 == fw.sum(0, 0)


def test_assign():
    fw = FenwickTree()
    fw = FenwickTree(10)


def test_zero():
    fw = FenwickTree(0)
    assert 0 == fw.sum(0, 0)


# def test_overflow_ull():
# overflowしないので実装しない


def test_naive_test():
    for n in range(51):
        fw = FenwickTree(n)
        for i in range(n):
            fw.add(i, i*i)
        for left in range(n+1):
            for right in range(left, n+1):
                total = 0
                for i in range(left, right):
                    total += i*i
                assert total == fw.sum(left, right)


# def test_smint():
# def test_mint():
# 実装しない


def test_invalid_assign():
    with pytest.raises(AssertionError) as e:
        fw = FenwickTree(-1)


@pytest.mark.parametrize("p", [
    [-1, 0],
    [10, 0]
])
def test_invalid_add(p):
    fw = FenwickTree(10)
    with pytest.raises(AssertionError) as e:
        fw.add(*p)


@pytest.mark.parametrize("p", [
    [-1, 3],
    [3, 11],
    [5, 3]
])
def test_invalid_sum(p):
    fw = FenwickTree(10)
    with pytest.raises(AssertionError) as e:
        fw.sum(*p)


def test_bound():
    fw = FenwickTree(10)
    fw.add(3, NUMERIC_MAX_INT)
    fw.add(5, NUMERIC_MIN_INT)
    assert -1 == fw.sum(0, 10)
    assert -1 == fw.sum(3, 6)
    assert NUMERIC_MAX_INT == fw.sum(3, 4)
    assert NUMERIC_MIN_INT == fw.sum(4, 10)


# def test_boundll():
# def test_overflow():
# def test_int128():
# 実装しない
