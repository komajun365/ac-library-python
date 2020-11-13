def ceil_pow2(n):
    """
    n <= 2**x を満たす最小のxを返却する。

    Parameters
    ----------
    n : int
        0以上の整数

    Returns
    -------
    int
        n <= 2**x を満たす最小のx

    """
    if n < 1:
        return 0
    return (n-1).bit_length()


def bsf(n):
    """
    自然数を2bitで表現したときに、右から見て最初に1が立つ桁が何桁目かを返却する。
    （0-indexed）

    Parameters
    ----------
    n : int
        1以上の整数

    Returns
    -------
    int
        2bitで表現したときに、右から見て最初に1が立つ桁（0-indexed）

    """
    return (n & -n).bit_length()-1
