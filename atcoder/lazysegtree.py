class LazySegTree:
    """
    遅延評価セグメントツリー
    https://github.com/atcoder/ac-library/blob/master/document_ja/lazysegtree.md

    Parameters
    ----------
    モノイドの型をS、写像の型をFとする。

    op : function(S, S) -> S
        S × S を計算する関数。二分木の二つの子から親を求める際に使う。
    e : function() -> S
        モノイドの初期値を返す関数。単位元。
    mapping : function(F, S) -> S
        反映させず遅延していた写像Fを適用する関数。
    composition : function(f: F, g: F) -> F
        f◦gで写像を更新する関数。
        元々あった写像がgで、新しく与えられる写像がf
    id : function() -> F
        写像の初期値を返す関数。
        composition(f, id()) = fを満たす必要がある。
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
    __init__(self, op, e, mapping, composition, id, n=0, v=[])
        初期化
    _update(self, k)
        子の情報から親(=_d[k])を更新する

        Parameters
        ----------
        k : int
            更新箇所
    _all_apply(self, k, f)
        _d[k]に写像fを反映させ、
        要素kが葉でないとき_lz[k]を初期化する。
        Parameters
        ----------
        k : int
            更新箇所
        f : F
    _push(self, k)
        _lz[k]を子に引き継ぎ、_lz[k]を初期化する。
        Parameters
        ----------
        k : int
            更新箇所
    set(self, p, x)
        p番目の要素をxで置き換える
        その際、関連する遅延要素の反映、値の更新を行う。
        Parameters
        ----------
        p : int
            0 <= p < self._n
            置き換える要素の番号。
        x : S
    get(self, p)
        p番目の要素の取得
        その際、関連する遅延要素の反映を行う。
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
    apply(self, p, f)
        p番目の要素に写像fを反映させる
        Parameters
        ----------
        p : int
            0 <= p < self._n
            写像を反映させる要素の番号
        f : F
            反映させたい写像
    apply_lr(self, left, right, f)
        ※本家ではapply関数にまとめているが、引数の数が異なるため本実装では分割
        l番目～r-1番目の要素に写像fを区間反映させる。
        （遅延要素として積み込む）
        Parameters
        ----------
        left : int
        right : int
            0 <= left <= right < self._n
        f : F
            反映させたい写像
    max_right(self, left, g)
        セグメントツリー上での二分探索結果を返却します。
        leftから始めて、右側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        left : int
            0 <= left <= self._n
            左側探索基準点
        g : function(S) -> bool
            g(e()) == Trueを満たす
        Returns
        -------
        int
            gが単調だとすれば、
            g(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最大のr
    min_left(self, right, g)
        セグメントツリー上での二分探索結果を返却します。
        rightから始めて、左側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        right : int
            0 <= right <= self._n
            →側探索基準点
        g : function(S) -> bool
            g(e()) == Trueを満たす
        Returns
        -------
        int
            gが単調だとすれば、
            g(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最小のl
    """
    def __init__(self, op, e, mapping, composition, id, n=0, v=[]):
        assert (len(v) >= 0) and (n >= 0)
        if len(v) == 0:
            v = [e() for _ in range(n)]
        self._n = len(v)
        self._log = (self._n - 1).bit_length()
        self._size = 1 << self._log
        self._d = [e() for _ in range(2 * self._size)]
        self._lz = [id() for _ in range(self._size)]
        self._op = op
        self._e = e
        self._mapping = mapping
        self._composition = composition
        self._id = id

        for i in range(self._n):
            self._d[self._size + i] = v[i]
        for i in range(self._size - 1, 0, -1):
            self._update(i)

    def _update(self, k):
        self._d[k] = self._op(self._d[2 * k], self._d[2 * k + 1])

    def _all_apply(self, k, f):
        self._d[k] = self._mapping(f, self._d[k])
        if k < self._size:
            self._lz[k] = self._composition(f, self._lz[k])

    def _push(self, k):
        self._all_apply(2*k, self._lz[k])
        self._all_apply(2*k+1, self._lz[k])
        self._lz[k] = self._id()

    def set(self, p, x):
        assert (0 <= p) and (p < self._n)
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = x
        for i in range(1, self._log + 1):
            self._update(p >> i)

    def get(self, p):
        assert (0 <= p) and (p < self._n)
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        return self._d[p]

    def prod(self, left, right):
        assert (0 <= left) and (left <= right) and (right <= self._n)
        if left == right:
            return self._e()

        left += self._size
        right += self._size

        for i in range(self._log, 0, -1):
            if((left >> i) << i) != left:
                self._push(left >> i)
            if((right >> i) << i) != right:
                self._push(right >> i)

        sml = self._e()
        smr = self._e()
        while left < right:
            if left & 1:
                sml = self._op(sml, self._d[left])
                left += 1
            if right & 1:
                right -= 1
                smr = self._op(self._d[right], smr)
            left //= 2
            right //= 2

        return self._op(sml, smr)

    def all_prod(self):
        return self._d[1]

    def apply(self, p, f):
        assert (0 <= p) and (p < self._n)
        p += self._size
        for i in range(self._log, 0, -1):
            self._push(p >> i)
        self._d[p] = self._mapping(f, self._d[p])
        for i in range(1, self._log+1):
            self._update(p >> i)

    def apply_lr(self, left, right, f):
        assert (0 <= left) and (left <= right) and (right <= self._n)
        if left == right:
            return

        left += self._size
        right += self._size

        for i in range(self._log, 0, -1):
            if((left >> i) << i) != left:
                self._push(left >> i)
            if((right >> i) << i) != right:
                self._push((right-1) >> i)

        left2, right2 = left, right
        while left < right:
            if left & 1:
                self._all_apply(left, f)
                left += 1
            if right & 1:
                right -= 1
                self._all_apply(right, f)
            left //= 2
            right //= 2
        left, right = left2, right2

        for i in range(1, self._log+1):
            if((left >> i) << i) != left:
                self._update(left >> i)
            if((right >> i) << i) != right:
                self._update((right-1) >> i)

    def max_right(self, left, g):
        assert (0 <= left) and (left <= self._n)
        assert g(self._e())
        if left == self._n:
            return self._n
        left += self._size
        for i in range(self._log, 0, -1):
            self._push(left >> i)
        sm = self._e()
        while True:
            while(left % 2 == 0):
                left //= 2
            if not g(self._op(sm, self._d[left])):
                while left < self._size:
                    self._push(left)
                    left *= 2
                    if g(self._op(sm, self._d[left])):
                        sm = self._op(sm, self._d[left])
                        left += 1
                return left - self._size
            sm = self._op(sm, self._d[left])
            left += 1
            if(left & -left) == left:
                break
        return self._n

    def min_left(self, right, g):
        assert (0 <= right) and (right <= self._n)
        assert g(self._e())
        if right == 0:
            return 0
        right += self._size
        for i in range(self._log, 0, -1):
            self._push((right-1) >> i)
        sm = self._e()
        while True:
            right -= 1
            while(right > 1) and (right % 2):
                right //= 2
            if not g(self._op(self._d[right], sm)):
                while right < self._size:
                    self._push(right)
                    right = 2 * right + 1
                    if g(self._op(self._d[right], sm)):
                        sm = self._op(self._d[right], sm)
                        right -= 1
                return right + 1 - self._size
            sm = self._op(self._d[right], sm)
            if(right & -right) == right:
                break
        return 0
