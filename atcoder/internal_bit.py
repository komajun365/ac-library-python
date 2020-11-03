#  @param n `0 <= n`
#  @return minimum non-negative `x` s.t. `n <= 2**x`
def ceil_pow2(n: int):
    if(n < 1):
        return 0
    return (n-1).bit_length()


# @param n `1 <= n`
# @return minimum non-negative `x` s.t. `(n & (1 << x)) != 0`
def bsf(n: int):
    return (n & -n).bit_length()-1
