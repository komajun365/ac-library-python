"""
数論的アルゴリズム詰め合わせ
https://atcoder.github.io/ac-library/production/document_ja/math.html
※pow_modは標準関数powで計算可能なため未作成
"""
from atcoder import inv_gcd


def inv_mod(x, m):
    """
    mを法としたときのxの逆元を計算する。

    Parameters
    ----------
    x : int
    m : int
        m >= 1 かつ x,mは互いに素

    Returns
    -------
    int
        mを法としたときのxの逆元
    """
    assert 1 <= m
    z = inv_gcd(x, m)
    assert z[0] == 1
    return z[1]


def crt(r, m):
    """
    中国余剰定理（Chinese Remainder Theorem, CRT）の計算
    len(r) = nとしたときに、
    全てのi(0 <= i < n)について、
    r[i] == x % m[i]を満たすxを計算する。

    Parameters
    ----------
    r : list = [int * n]
    m : list = [int * n]
        len(r) == len(m)
        1 <= m[i]

    Returns
    -------
    [r0, m0] : list
        答えが存在しない場合、[0, 0]
        len(r) == 0の時、[0,1]を返却する。
        それ以外の場合、
        全てのi(0 <= i < n)について、
        r[i] == x % m[i]を満たすxを計算し、
        x = r0 % m0が成り立つ[r0, m0]の組を返却する。
        m0 = lcm(m[i])となる。
    """
    assert len(r) == len(m)
    n = len(r)

    r0, m0 = 0, 1
    for i in range(n):
        assert 1 <= m[i]
        r1 = r[i] % m[i]
        m1 = m[i]
        if m0 < m1:
            r0, r1 = r1, r0
            m0, m1 = m1, m0
        if m0 % m1 == 0:
            if r0 % m1 != r1:
                return [0, 0]
            continue

        g, im = inv_gcd(m0, m1)
        u1 = m1 // g
        if (r1 - r0) % g:
            return [0, 0]

        x = (r1 - r0) // g % u1 * im % u1
        r0 += x * m0
        m0 *= u1
        if r0 < 0:
            r0 += m0
    return [r0, m0]


def floor_sum(n, m, a, b):
    """
    Σ^{n-1}_{0} ((a*i+b)//m)を計算する。

    Parameters
    ----------
    n : int
    m : int
    a : int
    b : int
        0 <= n
        1 <= m
        0 <= a,b < m

    Returns
    -------
    ans : int
    """
    ans = 0
    while True:
        if a >= m:
            ans += (n - 1) * n * (a // m) // 2
            a %= m
        if b >= m:
            ans += n * (b // m)
            b %= m

        y_max = (a * n + b) // m
        x_max = y_max * m - b
        if y_max == 0:
            return ans
        ans += (n - (x_max + a - 1) // a) * y_max
        n, m, a, b = y_max, a, m, (a - x_max % a) % a
