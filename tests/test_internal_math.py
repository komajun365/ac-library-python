from atcoder import is_prime, inv_gcd, primitive_root
from tests.utils.math_ import is_primitive_root
from math import gcd


NUMERIC_MAX_INT = 2**31 - 1
NUMERIC_MAX_LL = 2**63 - 1
NUMERIC_MIN_LL = -1 * 2**63


def is_prime_naive(n):
    assert 0 <= n <= NUMERIC_MAX_INT
    if n == 0 or n == 1:
        return False

    m = int(n ** 0.5)
    for i in range(2, m+1):
        if n % i == 0:
            return False
    return True


def test_is_prime():
    assert not is_prime(121)
    assert not is_prime(11 * 13)
    assert is_prime(1000000007)
    assert not is_prime(1000000008)
    assert is_prime(1000000009)
    for i in range(10000):
        assert is_prime_naive(i) == is_prime(i)

    for i in range(10000):
        x = NUMERIC_MAX_INT - i
        assert is_prime_naive(x) == is_prime(x)


def test_inv_gcd():
    pred = []
    for i in range(11):
        pred.append(i)
        pred.append(-i)
        pred.append(NUMERIC_MIN_LL + i)
        pred.append(NUMERIC_MAX_LL - i)

        pred.append(NUMERIC_MIN_LL // 2 + i)
        pred.append(NUMERIC_MIN_LL // 2 - i)
        pred.append(NUMERIC_MAX_LL // 2 + i)
        pred.append(NUMERIC_MAX_LL // 2 - i)

        pred.append(NUMERIC_MIN_LL // 3 + i)
        pred.append(NUMERIC_MIN_LL // 3 - i)
        pred.append(NUMERIC_MAX_LL // 3 + i)
        pred.append(NUMERIC_MAX_LL // 3 - i)

    pred.append(998244353)
    pred.append(1000000007)
    pred.append(1000000009)
    pred.append(-998244353)
    pred.append(-1000000007)
    pred.append(-1000000009)

    for a in pred:
        for b in pred:
            if b <= 0:
                continue
            a2 = a % b
            eg = inv_gcd(a, b)
            g = gcd(a, b)
            assert g == eg[0]
            assert 0 <= eg[1]
            assert eg[1] <= b // eg[0]
            assert g % b == eg[1] * a2 % b


def test_primitive_root_naive():
    for m in range(2, 10001):
        if is_prime(m):
            n = primitive_root(m)
            assert 1 <= n
            assert n < m
            x = 1
            for _ in range(1, m-1):
                x = x*n % m
                assert x != 1

            x = x*n % m
            assert x == 1


def test_primitive_root_template():
    assert is_primitive_root(2, primitive_root(2))
    assert is_primitive_root(3, primitive_root(3))
    assert is_primitive_root(5, primitive_root(5))
    assert is_primitive_root(7, primitive_root(7))
    assert is_primitive_root(11, primitive_root(11))
    assert is_primitive_root(998244353, primitive_root(998244353))
    assert is_primitive_root(1000000007, primitive_root(1000000007))
    assert is_primitive_root(469762049, primitive_root(469762049))
    assert is_primitive_root(167772161, primitive_root(167772161))
    assert is_primitive_root(754974721, primitive_root(754974721))
    assert is_primitive_root(324013369, primitive_root(324013369))
    assert is_primitive_root(831143041, primitive_root(831143041))
    assert is_primitive_root(1685283601, primitive_root(1685283601))


def test_primitive_root():
    for i in range(1000):
        x = NUMERIC_MAX_INT - i
        if is_prime(x):
            assert is_primitive_root(x, primitive_root(x))
