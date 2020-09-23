'''
長さ N の配列に対し、
・要素の 1 点変更(加算)
・区間の要素の総和
を O(logN) で求めることが出来るデータ構造です。

要素はintとしておきます。
※modを設定し、modintっぽく振る舞うようにしておきます。

初期値は0。

'''


class FenwickTree:
    def __init__(self, n: int, mod: int = 0):
        self.__mod = mod
        self.__n = n
        self.__data = [0] * self.__n

    def add(self, p: int, x: int):
        assert (0 <= p) & (p < self.__n)
        if(self.__mod == 0):
            self.__add_mod0(p, x)
        else:
            self.__add_mod(p, x)

    def __add_mod0(self, p: int, x: int):
        p += 1
        while(p <= self.__n):
            self.__data[p - 1] += x
            p += p & -p

    def __add_mod(self, p: int, x: int):
        p += 1
        while(p <= self.__n):
            self.__data[p - 1] += x
            self.__data[p - 1] %= self.__mod
            p += p & -p

    def sum(self, l: int, r: int):
        assert (0 <= l) & (l <= r) & (r <= self.__n)
        if(self.__mod == 0):
            return self.__sum_mod0(r) - self.__sum_mod0(l)
        else:
            return (self.__sum_mod(r) - self.__sum_mod(l)) % self.__mod

    def __sum_mod0(self, r: int):
        s = 0
        while(r > 0):
            s += self.__data[r - 1]
            r -= r & -r
        return s

    def __sum_mod(self, r: int):
        s = 0
        while(r > 0):
            s += self.__data[r - 1]
            s %= self.__mod
            r -= r & -r
        return s
