"""
文字列アルゴリズムの詰め合わせ
https://atcoder.github.io/ac-library/production/document_ja/string.html
・suffix_array
・lcp_array
・z_algorithm
"""


def sa_naive(s):
    """
    sa_is()の内部呼び出し用関数。
    文字数がTHRESHOLD_NAIVE未満のときにナイーブに処理する。

    Parameters
    ----------
    s : list
        文字列を整数列に変換したもの
    Returns
    -------
    sa : list
        sのsuffix array
    """
    n = len(s)
    sa = list(range(n))
    sa.sort(key=lambda x: s[x:])
    return sa


def sa_doubling(s):
    """
    sa_is()の内部呼び出し用関数。
    文字数がTHRESHOLD_NAIVE以上THRESHOLD_DOUBLINGのときにダブリングで処理する。

    Parameters
    ----------
    s : list
        文字列を整数列に変換したもの
    Returns
    -------
    sa : list
        sのsuffix array
    """
    n = len(s)
    n_plus = n + 10
    sa = list(range(n))
    rnk = s[::]
    tmp = [0] * n
    k = 1
    while k < n:
        def cmp(x):
            first = rnk[x] * n_plus
            second = -1 if (x + k >= n) else rnk[x + k]
            return first + second
        sa.sort(key=cmp)
        tmp[sa[0]] = 0
        for i in range(1, n):
            tmp[sa[i]] = tmp[sa[i - 1]] + (cmp(sa[i]) > cmp(sa[i - 1]))
        rnk, tmp = tmp, rnk
        k *= 2
    return sa


def sa_is(s, upper):
    """
    suffix_array()の内部呼び出し用関数。
    文字数がTHRESHOLD_DOUBLING以上のときはSA-ISアルゴリズムで処理する。
    それ以下の場合は別の関数を呼び出す。

    Parameters
    ----------
    s : list
        文字列を整数列に変換したもの
    upper : int
        文字を整数に変換した場合の最大値。
        文字は0~upperまでの最大(upper+1)種類しか出現しないとみなす。
    Returns
    -------
    sa : list
        sのsuffix array
    """
    THRESHOLD_NAIVE = 10
    THRESHOLD_DOUBLING = 40

    n = len(s)
    if n == 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        if s[0] < s[1]:
            return [0, 1]
        else:
            return [1, 0]

    if n < THRESHOLD_NAIVE:
        return sa_naive(s)
    elif n < THRESHOLD_DOUBLING:
        return sa_doubling(s)

    sa = [0] * n
    ls = [0] * n
    for i in range(n - 2, -1, -1):
        ls[i] = ls[i + 1] if s[i] == s[i + 1] else s[i] < s[i + 1]
    sum_l = [0] * (upper + 1)
    sum_s = [0] * (upper + 1)
    for i in range(n):
        if not ls[i]:
            sum_s[s[i]] += 1
        else:
            sum_l[s[i] + 1] += 1
    for i in range(upper):
        sum_s[i] += sum_l[i]
        if i < upper:
            sum_l[i + 1] += sum_s[i]

    def induce(lms):
        nonlocal sa, sum_s, sum_l
        sa = [-1] * n
        buf = sum_s[::]
        for d in lms:
            if d == n:
                continue
            sa[buf[s[d]]] = d
            buf[s[d]] += 1
        buf = sum_l[::]
        sa[buf[s[n - 1]]] = n - 1
        buf[s[n - 1]] += 1
        for i in range(n):
            v = sa[i]
            if v >= 1 and not ls[v - 1]:
                sa[buf[s[v - 1]]] = v - 1
                buf[s[v - 1]] += 1
        buf = sum_l[::]
        for i in range(n - 1, -1, -1):
            v = sa[i]
            if v >= 1 and ls[v - 1]:
                buf[s[v - 1] + 1] -= 1
                sa[buf[s[v - 1] + 1]] = v - 1

    lms_map = [-1] * (n + 1)
    m = 0
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms_map[i] = m
            m += 1
    lms = []
    for i in range(1, n):
        if not ls[i - 1] and ls[i]:
            lms.append(i)

    induce(lms)

    if m:
        sorted_lms = []
        for v in sa:
            if lms_map[v] != -1:
                sorted_lms.append(v)
        rec_s = [0] * m
        rec_upper = 0
        rec_s[lms_map[sorted_lms[0]]] = 0
        for i in range(1, m):
            left, right = sorted_lms[i - 1:i + 1]
            end_l = lms[lms_map[left] + 1] if (lms_map[left] + 1 < m) else n
            end_r = lms[lms_map[right] + 1] if (lms_map[right] + 1 < m) else n
            same = True
            if end_l - left != end_r - right:
                same = False
            else:
                while left < end_l:
                    if s[left] != s[right]:
                        break
                    left += 1
                    right += 1
                if left == n:
                    same = False
                elif s[left] != s[right]:
                    same = False
            if not same:
                rec_upper += 1
            rec_s[lms_map[sorted_lms[i]]] = rec_upper

        rec_sa = sa_is(rec_s, rec_upper)

        for i in range(m):
            sorted_lms[i] = lms[rec_sa[i]]

        induce(sorted_lms)

    return sa


def suffix_array(s, upper=-1):
    """
    suffix_arrayを計算する。
    入力形式ごとの前処理を行い、sa_is()関数に引き渡す。

    Parameters
    ----------
    s : str or list
        文字列あるいは、文字列を整数列に変換したもの
    upper : int
        文字を整数に変換した場合の最大値。
        文字は0~upperまでの最大(upper+1)種類しか出現しないとみなす。
        未入力の場合は内部でupperを算出する。
    Returns
    -------
    sa : list
        sのsuffix array
    """
    n = len(s)
    if type(s) is list and upper >= 0:
        assert 0 <= min(s) and max(s) <= upper
        return sa_is(s, upper)

    elif type(s) is list and upper == -1:
        idx = list(range(n))
        idx.sort(key=lambda x: s[x])
        s2 = [0] * n
        now = 0
        for i in range(n):
            if i and s[idx[i - 1]] != s[idx[i]]:
                now += 1
            s2[idx[i]] = now
        return sa_is(s2, now)

    elif type(s) is str:
        s2 = [0] * n
        for i, si in enumerate(s):
            s2[i] = ord(si)
        return sa_is(s2, 255)

    else:
        print('type error')
        assert False


def lcp_array(s, sa):
    """
    lcp arrayを計算する。

    Parameters
    ----------
    s : str or list
        文字列あるいは、文字列を整数列に変換したもの
    sa : list
        sのsuffix array
    Returns
    -------
    lcp : list
        sのlcp array
    """
    n = len(s)
    assert n >= 1
    if type(s) is str:
        s2 = [0] * n
        for i, si in enumerate(s):
            s2[i] = ord(si)
        s = s2

    rnk = [0] * n
    for i, sai in enumerate(sa):
        rnk[sai] = i
    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        if h > 0:
            h -= 1
        if rnk[i] == 0:
            continue
        j = sa[rnk[i] - 1]
        while j + h < n and i + h < n:
            if s[j + h] != s[i + h]:
                break
            h += 1
        lcp[rnk[i] - 1] = h
    return lcp


def z_algorithm(s):
    """
    z_algorithmの計算を行う。

    Parameters
    ----------
    s : str or list
        文字列あるいは、文字列を整数列に変換したもの
    Returns
    -------
    z : list
        z[i]はs[:]とs[i:]のLCPの長さ。
    """
    n = len(s)
    if n == 0:
        return []
    if type(s) is str:
        s2 = [0] * n
        for i, si in enumerate(s):
            s2[i] = ord(si)
        s = s2
    z = [0] * n
    j = 0
    for i in range(1, n):
        z[i] = 0 if (j + z[j] <= i) else min(j + z[j] - i, z[i - j])
        while i + z[i] < n:
            if s[z[i]] != s[i + z[i]]:
                break
            z[i] += 1
        if j + z[j] < i + z[i]:
            j = i
    z[0] = n
    return z
