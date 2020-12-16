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
