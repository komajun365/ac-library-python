from atcoder import ceil_pow2, bsf


def test_ceilpow2():
    assert ceil_pow2(0) == 0
    assert ceil_pow2(1) == 0
    assert ceil_pow2(2) == 1
    assert ceil_pow2(3) == 2
    assert ceil_pow2(4) == 2
    assert ceil_pow2(5) == 3
    assert ceil_pow2(6) == 3
    assert ceil_pow2(7) == 3
    assert ceil_pow2(8) == 3
    assert ceil_pow2(9) == 4
    assert ceil_pow2(1 << 30) == 30
    assert ceil_pow2((1 << 30)+1) == 31
    int_max = 2147483647
    assert ceil_pow2(int_max) == 31


def test_bsf():
    assert bsf(1) == 0
    assert bsf(2) == 1
    assert bsf(3) == 0
    assert bsf(4) == 2
    assert bsf(5) == 0
    assert bsf(6) == 1
    assert bsf(7) == 0
    assert bsf(8) == 3
    assert bsf(9) == 0
    assert bsf(1 << 30) == 30
    assert bsf((1 << 31)-1) == 0
    assert bsf(1 << 31) == 31
    int_max = 2147483647
    assert bsf(int_max) == 0