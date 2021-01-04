from atcoder import inv_mod, crt, floor_sum
from math import gcd
import itertools

NUMERIC_MAX_LL = 2**63 - 1
NUMERIC_MIN_LL = -1 * 2**63


def floor_sum_naive(n, m, a, b):
    sum = 0
    for i in range(n):
        sum += (a * i + b) // m
    return sum


def test_inv_bound_hand():
    assert inv_mod(-1, NUMERIC_MAX_LL) == inv_mod(NUMERIC_MIN_LL,
                                                  NUMERIC_MAX_LL)
    assert 1 == inv_mod(NUMERIC_MAX_LL, NUMERIC_MAX_LL - 1)
    assert NUMERIC_MAX_LL - 1 == inv_mod(NUMERIC_MAX_LL - 1, NUMERIC_MAX_LL)
    assert 2 == inv_mod(NUMERIC_MAX_LL // 2 + 1, NUMERIC_MAX_LL)


def test_inv_mod():
    for a in range(-100, 101):
        for b in range(1, 1001):
            if gcd(a % b, b) != 1:
                continue
            c = inv_mod(a, b)
            assert 0 <= c
            assert c < b
            assert 1 % b == a * c % b


def test_inv_mod_zero():
    assert 0 == inv_mod(0, 1)
    for i in range(10):
        assert 0 == inv_mod(i, 1)
        assert 0 == inv_mod(-i, 1)
        assert 0 == inv_mod(NUMERIC_MIN_LL + i, 1)
        assert 0 == inv_mod(NUMERIC_MAX_LL - i, 1)


def test_floor_sum():
    for n in range(20):
        for m in range(1, 20):
            for a in range(20):
                for b in range(20):
                    assert floor_sum_naive(n, m, a, b) == floor_sum(n, m, a, b)


def test_crt_hand():
    res = crt([1, 2, 1], [2, 3, 2])
    assert res[0] == 5
    assert res[1] == 6


def test_crt2():
    for a in range(1, 21):
        for b in range(1, 21):
            for c in range(-10, 11):
                for d in range(-10, 11):
                    res = crt([c, d], [a, b])
                    if res[1] == 0:
                        for x in range(a * b // gcd(a, b)):
                            assert x % a != c or x % b != d
                        continue
                    assert a * b // gcd(a, b) == res[1]
                    assert c % a == res[0] % a
                    assert d % b == res[0] % b


def test_crt3():
    for a in range(1, 6):
        for b in range(1, 6):
            for c in range(1, 6):
                for d in range(-5, 6):
                    for e in range(-5, 6):
                        for f in range(-5, 6):
                            res = crt([d, e, f], [a, b, c])
                            lcm = a * b // gcd(a, b)
                            lcm = lcm * c // gcd(lcm, c)
                            if res[1] == 0:
                                for x in range(lcm):
                                    assert (x % a != d or
                                            x % b != e or
                                            x % c != f)
                                continue
                            assert lcm == res[1]
                            assert d % a == res[0] % a
                            assert e % b == res[0] % b
                            assert f % c == res[0] % c


def test_crt_overflow():
    r0 = 0
    r1 = 10**12 - 2
    m0 = 900577
    m1 = 10**12
    res = crt([r0, r1], [m0, m1])
    assert m0 * m1 == res[1]
    assert r0 == res[0] % m0
    assert r1 == res[0] % m1


def test_crt_bound():
    inf = NUMERIC_MAX_LL
    pred = []
    for i in range(1, 11):
        pred.append(i)
        pred.append(inf - (i - 1))
    pred.append(998244353)
    pred.append(1_000_000_007)
    pred.append(1_000_000_009)

    for ab in [[inf, inf],
               [1, inf],
               [inf, 1],
               [7, inf],
               [inf // 337, 337],
               [2, (inf - 1) // 2]]:
        a, b = ab
        for ph in range(2):
            for ans in pred:
                res = crt([ans % a, ans % b], [a, b])
                lcm = a // gcd(a, b) * b
                assert lcm == res[1]
                assert ans % lcm == res[0]
            a, b = b, a

    factor_inf = [49, 73, 127, 337, 92737, 649657]
    for p in itertools.permutations(factor_inf):
        p = list(p)
        for ans in pred:
            r = []
            m = []
            for f in p:
                r.append(ans % f)
                m.append(f)
            res = crt(r, m)
            assert ans % inf == res[0]
            assert inf == res[1]

    factor_infn1 = [2, 3, 715827883, 2147483647]
    for p in itertools.permutations(factor_infn1):
        p = list(p)
        for ans in pred:
            r = []
            m = []
            for f in p:
                r.append(ans % f)
                m.append(f)
            res = crt(r, m)
            assert ans % (inf - 1) == res[0]
            assert inf - 1 == res[1]
