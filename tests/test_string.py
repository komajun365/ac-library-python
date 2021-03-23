from atcoder import sa_naive, sa_doubling, sa_is, suffix_array, \
    lcp_array, z_algorithm

NUMERIC_MAX_INT = 2**31 - 1
NUMERIC_MIN_INT = -1 * 2**31
NUMERIC_MAX_UINT = 2**32 - 1
NUMERIC_MIN_UINT = 0
NUMERIC_MAX_LL = 2**63 - 1
NUMERIC_MIN_LL = -1 * 2**63
NUMERIC_MAX_ULL = 2**64 - 1
NUMERIC_MIN_ULL = 0


def sa_naive_test(s):
    n = len(s)
    sa = list(range(n))
    sa.sort(key=lambda x: s[x:])
    return sa


def lcp_naive(s, sa):
    n = len(s)
    assert n
    lcp = [0] * (n-1)
    for i in range(n-1):
        left = sa[i]
        right = sa[i+1]
        while left + lcp[i] < n and right + lcp[i] < n and \
                s[left + lcp[i]] == s[right + lcp[i]]:
            lcp[i] += 1
    return lcp


def z_naive(s):
    n = len(s)
    z = [0] * n
    for i in range(n):
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
    return z


def test_empty():
    assert [] == suffix_array('')
    assert [] == suffix_array([])
    assert [] == z_algorithm('')
    assert [] == z_algorithm([])


def test_sa_lcp_naive():
    for n in range(1, 6):
        m = 1
        for i in range(n):
            m *= 4
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 4
                max_c = max(max_c, s[i])
                g //= 4
            sa = sa_naive_test(s)
            assert sa == suffix_array(s)
            assert sa == suffix_array(s, max_c)
            assert lcp_naive(s, sa) == lcp_array(s, sa)
    for n in range(1, 11):
        m = 1
        for i in range(n):
            m *= 2
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 2
                max_c = max(max_c, s[i])
                g //= 2
            sa = sa_naive(s)
            assert sa == suffix_array(s)
            assert sa == suffix_array(s, max_c)
            assert lcp_naive(s, sa) == lcp_array(s, sa)


def test_internal_sanaive_naive():
    for n in range(1, 6):
        m = 1
        for i in range(n):
            m *= 4
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 4
                max_c = max(max_c, s[i])
                g //= 4
            assert sa_naive(s) == sa_naive_test(s)
    for n in range(1, 11):
        m = 1
        for i in range(n):
            m *= 2
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 2
                max_c = max(max_c, s[i])
                g //= 2
        assert sa_naive(s) == sa_naive_test(s)


def test_internal_sadoubling_naive():
    for n in range(1, 6):
        m = 1
        for i in range(n):
            m *= 4
        for f in range(m):
            s = [0] * n
            g = f
            for i in range(n):
                s[i] = g % 4
                g //= 4
            assert sa_naive(s) == sa_doubling(s)
    for n in range(1, 11):
        m = 1
        for i in range(n):
            m *= 2
        for f in range(m):
            s = [0] * n
            g = f
            for i in range(n):
                s[i] = g % 2
                g //= 2
        assert sa_naive(s) == sa_doubling(s)


def test_internal_sais_naive():
    for n in range(1, 6):
        m = 1
        for i in range(n):
            m *= 4
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 4
                max_c = max(max_c, s[i])
                g //= 4
            assert sa_naive(s) == sa_is(s, max_c)
    for n in range(1, 11):
        m = 1
        for i in range(n):
            m *= 2
        for f in range(m):
            s = [0] * n
            g = f
            max_c = 0
            for i in range(n):
                s[i] = g % 2
                max_c = max(max_c, s[i])
                g //= 2
        assert sa_naive(s) == sa_is(s, max_c)


def test_sa_allAB_test():
    for n in range(1, 101):
        s = [0] * n
        for i in range(n):
            s[i] = i % 2
        assert sa_naive_test(s) == suffix_array(s)
        assert sa_naive_test(s) == suffix_array(s, 3)
    for n in range(1, 101):
        s = [0] * n
        for i in range(n):
            s[i] = 1 - i % 2
        assert sa_naive_test(s) == suffix_array(s)
        assert sa_naive_test(s) == suffix_array(s, 3)


def test_sa():
    s = 'missisippi'

    sa = suffix_array(s)

    answer = [
        'i',
        'ippi',
        'isippi',
        'issisippi',
        'missisippi',
        'pi',
        'ppi',
        'sippi',
        'sisippi',
        'ssisippi'
    ]

    assert len(answer) == len(sa)

    for i in range(len(sa)):
        assert answer[i] == s[sa[i]:]


def test_sa_single():
    assert [0] == suffix_array([0])
    assert [0] == suffix_array([-1])
    assert [0] == suffix_array([1])
    assert [0] == suffix_array([NUMERIC_MIN_INT])
    assert [0] == suffix_array([NUMERIC_MAX_INT])


def test_lcp():
    s = 'aab'
    sa = suffix_array(s)
    assert [0, 1, 2] == sa
    lcp = lcp_array(s, sa)
    assert [1, 0] == lcp

    assert lcp == lcp_array([0, 0, 1], sa)
    assert lcp == lcp_array([-100, -100, 100], sa)
    assert lcp == lcp_array([NUMERIC_MIN_INT,
                             NUMERIC_MIN_INT,
                             NUMERIC_MAX_INT],
                            sa)
    assert lcp == lcp_array([NUMERIC_MIN_LL,
                             NUMERIC_MIN_LL,
                             NUMERIC_MAX_LL],
                            sa)
    assert lcp == lcp_array([NUMERIC_MIN_UINT,
                             NUMERIC_MIN_UINT,
                             NUMERIC_MAX_UINT],
                            sa)
    assert lcp == lcp_array([NUMERIC_MIN_ULL,
                             NUMERIC_MIN_ULL,
                             NUMERIC_MAX_ULL],
                            sa)


def test_z_algo():
    s = 'abab'
    z = z_algorithm(s)
    assert [4, 0, 2, 0] == z
    assert [4, 0, 2, 0] == z_algorithm([1, 10, 1, 10])
    assert z_naive([0] * 7) == z_algorithm([0] * 7)


def test_z_naive():
    for n in range(1, 6):
        m = 1
        for i in range(n):
            m *= 4
        for f in range(m):
            s = [0] * n
            g = f
            for i in range(n):
                s[i] = g % 4
                g //= 4
            assert z_naive(s) == z_algorithm(s)
    for n in range(1, 11):
        m = 1
        for i in range(n):
            m *= 2
        for f in range(m):
            s = [0] * n
            g = f
            for i in range(n):
                s[i] = g % 2
                g //= 2
        assert z_naive(s) == z_algorithm(s)
