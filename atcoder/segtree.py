class SegTree:
    """
    セグメントツリー
    https://atcoder.github.io/ac-library/production/document_ja/segtree.html

    Parameters
    ----------
    モノイドの型をSとする。

    op : function(S, S) -> S
        S × S を計算する関数。二分木の二つの子から親を求める際に使う。
    e : function() -> S
        モノイドの初期値を返す関数。単位元。
    n : int
        セグメントツリーで管理する要素数。n>=0を満たす。
        vが与えられない場合に参照する。要素は全てe()で初期化される。
    v : list[S]
        セグメントツリーで管理する要素の初期値
        vが与えられた場合nは無視する

    Attributes
    ----------
    _n : int
        セグメントツリーで管理する要素数
    _log : int
        _n <= 2**x を満たす最小のx
    _size : int
        1 << self._log
        セグメントツリー全体のサイズ
    _d : list[S]
        セグメントツリーで管理するモノイドを並べたリスト
        _d[1]が根に当たり、_d[x]の子は_d[x*2]と_d[x*2+1]になる。
    _lz : list[S]
        セグメントツリーで管理する遅延要素（写像）を並べたリスト
        _lz[1]が根に当たり、_lz[x]の子は_lz[x*2]と_lz[x*2+1]になる。
        サイズが_dの半分（セグメントツリーの葉には対応する遅延要素はないため。）
    _op : function(S, S)
    _e : function()
    _mapping : function(F, S)
    _composition : function(F, F)
    _id : function()
        それぞれParametersを参照

    Methods
    -------
    __init__(self, op, e, n=None, v=None)
        初期化
    _update(self, k)
        子の情報から親(=_d[k])を更新する

        Parameters
        ----------
        k : int
            更新箇所
    set(self, p, x)
        p番目の要素をxで置き換える
        その際、関連する値の更新を行う。
        Parameters
        ----------
        p : int
            0 <= p < self._n
            置き換える要素の番号。
        x : S
    get(self, p)
        p番目の要素の取得
        Parameters
        ----------
        p : int
            0 <= p < self._n
            置き換える要素の番号。
        Returns
        -------
        S
            self._d[p]
    prod(self, left, right)
        l番目～r-1番目の要素の演算結果
        Parameters
        ----------
        left : int
        right : int
            0 <= left <= right < self._n
        Returns
        -------
        S
            l番目～r-1番目の要素の演算結果
            l==rの場合はe()を返却する。
    all_prod(self)
        0番目～n-1番目の要素の演算結果
        Returns
        -------
        S
            0番目～n-1番目の要素の演算結果
    max_right(self, left, f)
        セグメントツリー上での二分探索結果を返却します。
        leftから始めて、右側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        left : int
            0 <= left <= self._n
            左側探索基準点
        f : function(S) -> bool
            f(e()) == Trueを満たす
        Returns
        -------
        int
            fが単調だとすれば、
            f(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最大のr
    min_left(self, right, f)
        セグメントツリー上での二分探索結果を返却します。
        rightから始めて、左側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        right : int
            0 <= right <= self._n
            右側探索基準点
        f : function(S) -> bool
            f(e()) == Trueを満たす
        Returns
        -------
        int
            fが単調だとすれば、
            f(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最小のl
    """
    def __init__(self, op, e, n=None, v=None):
        if n is None and v is None:
            v = []
        elif n is None:
            assert len(v) >= 0
        elif v is None:
            assert n >= 0
            v = [e()] * n
        self.__n = len(v)
        self.__log = (self.__n - 1).bit_length()
        self.__size = 1 << self.__log
        self.__d = [e()] * (2 * self.__size)
        self.__op = op
        self.__e = e
        for i in range(self.__n):
            self.__d[self.__size + i] = v[i]
        for i in range(self.__size - 1, 0, -1):
            self.__update(i)

    def __update(self, k):
        self.__d[k] = self.__op(self.__d[2 * k], self.__d[2 * k + 1])

    def set(self, p, x):
        assert 0 <= p and p < self.__n
        p += self.__size
        self.__d[p] = x
        for i in range(1, self.__log + 1):
            self.__update(p >> i)

    def get(self, p):
        assert 0 <= p and p < self.__n
        return self.__d[p + self.__size]

    def prod(self, left, right):
        assert 0 <= left <= right <= self.__n
        sml = self.__e()
        smr = self.__e()
        left += self.__size
        right += self.__size

        while(left < right):
            if left & 1:
                sml = self.__op(sml, self.__d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self.__op(self.__d[right], smr)
            left //= 2
            right //= 2

        return self.__op(sml, smr)

    def all_prod(self):
        return self.__d[1]

    def max_right(self, left, f):
        assert 0 <= left <= self.__n
        assert f(self.__e())
        if left == self.__n:
            return self.__n
        left += self.__size
        sm = self.__e()
        while True:
            while left % 2 == 0:
                left //= 2
            if not f(self.__op(sm, self.__d[left])):
                while left < self.__size:
                    left *= 2
                    if f(self.__op(sm, self.__d[left])):
                        sm = self.__op(sm, self.__d[left])
                        left += 1
                return left - self.__size
            sm = self.__op(sm, self.__d[left])
            left += 1
            if (left & -left) == left:
                break
        return self.__n

    def min_left(self, right, f):
        assert 0 <= right <= self.__n
        assert f(self.__e())
        if right == 0:
            return 0
        right += self.__size
        sm = self.__e()
        while True:
            right -= 1
            while right > 1 and right % 2:
                right //= 2
            if not f(self.__op(self.__d[right], sm)):
                while right < self.__size:
                    right = 2 * right + 1
                    if f(self.__op(self.__d[right], sm)):
                        sm = self.__op(self.__d[right], sm)
                        right -= 1
                return right + 1 - self.__size
            sm = self.__op(self.__d[right], sm)
            if (right & -right) == right:
                break
        return 0
