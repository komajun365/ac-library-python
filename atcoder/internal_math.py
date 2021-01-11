def is_prime(n):
    """
    正の整数nが素数かどうかを判定する

    Parameters
    ----------
    n : int
        正の整数

    Returns
    -------
    bool
        nが素数であればTrue, そうでなければFalse
    """
    if n <= 1:
        return False
    if n == 2 or n == 7 or n == 61:
        return True
    if n % 2 == 0:
        return False

    d = n - 1
    while d % 2 == 0:
        d //= 2

    bases = [2, 7, 61]
    for a in bases:
        t = d
        y = pow(a, t, n)
        while t != n-1 and y != 1 and y != n-1:
            y = y*y % n
            t <<= 1

        if y != n-1 and t % 2 == 0:
            return False

    return True


def inv_gcd(a, b):
    """
    g = gcd(a, b), xa = g (mod b), 0 <= x < b/g
    を満たすような[g, x]を計算する。
    特にg = gcd(a, b) = 1 の時、
    xはbを法としたときのaの逆元である。
    a = 0 の場合は[b, 0]を返却する。

    Parameters
    ----------
    a : int
    b : int
        b >= 1

    Returns
    -------
    [s, m0] : list
    """
    a %= b
    if a == 0:
        return [b, 0]

    s, t = b, a
    m0, m1 = 0, 1
    while t:
        u = s // t
        s -= t * u
        m0 -= m1 * u
        s, t = t, s
        m0, m1 = m1, m0

    if m0 < 0:
        m0 += b // s
    return [s, m0]


def primitive_root(m):
    """
    整数mの最小原始根を計算する

    Parameters
    ----------
    m : int
        2以上の整数

    Returns
    -------
    int
        mの最小原始根
    """
    if m == 2:
        return 1
    if m == 167772161:
        return 3
    if m == 469762049:
        return 3
    if m == 754974721:
        return 11
    if m == 998244353:
        return 3

    divs = [2] + [0] * 19
    cnt = 1
    x = (m - 1) // 2
    while x % 2 == 0:
        x //= 2

    i = 3
    while i**2 <= x:
        if x % i == 0:
            divs[cnt] = i
            cnt += 1
            while x % i == 0:
                x //= i

        i += 2

    if x > 1:
        divs[cnt] = x
        cnt += 1

    g = 2
    while True:
        for i in range(cnt):
            if pow(g, (m-1)//divs[i], m) == 1:
                break

        else:
            return g

        g += 1
