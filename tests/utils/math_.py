def factors(m):
    """
    正の整数mの素因数を列挙する。

    Parameters
    ----------
    m : int
        正の整数

    Returns
    -------
    result : list
        mの素因数が格納されたリスト
    """
    result = []
    n = int(m ** 0.5)
    for i in range(2, n+1):
        if m % i == 0:
            result.append(i)
            while m % i == 0:
                m //= i
    if m > 1:
        result.append(m)
    return result


def is_primitive_root(m, g):
    """
    gがmの原始根であるかどうかを判定する

    Parameters
    ----------
    m : int
        正の整数
    g : int
        1以上, m未満の整数

    Returns
    -------
    bool
        gがmの原始根であればTrue、そうでなければFalse
    """
    assert 1 <= g < m
    for x in factors(m - 1):
        if pow(g, (m-1)//x, m) == 1:
            return False
    return True
