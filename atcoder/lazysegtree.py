class LazySegTree:
    '''
    遅延評価セグメントツリー
    https://github.com/atcoder/ac-library/blob/master/document_ja/lazysegtree.md

    Parameters
    ----------
    モノイドの型をS、写像の型をFとする。

    op : function(S, S) -> S
        S × S を計算する関数。二分木の二つの子から親を求める際に使う。
    e : function() -> S
        モノイドの初期値を返す関数。単位元。
    mapping : function(S, F) -> S
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
    __n : int
        セグメントツリーで管理する要素数
    __log : int
        __n <= 2**x を満たす最小のx
    __size : int
        1 << self.__log
        セグメントツリー全体のサイズ
    __d : list[S]
        セグメントツリーで管理するモノイドを並べたリスト
        __d[1]が根に当たり、__d[x]の子は__d[x*2]と__d[x*2+1]になる。
    __lz : list[S]
        セグメントツリーで管理する遅延要素（写像）を並べたリスト
        __lz[1]が根に当たり、__lz[x]の子は__lz[x*2]と__lz[x*2+1]になる。
        サイズが__dの半分（セグメントツリーの葉には対応する遅延要素はないため。）
    __op : function(S, S)
    __e : function()
    __mapping : function(S, F)
    __composition : function(F, F)
    __id : function()
        それぞれParametersを参照

    Methods
    -------
    __init__(self, op, e, mapping, composition, id, n=0, v=[])
        初期化
    __update(self, k)
        子の情報から親(=__d[k])を更新する

        Parameters
        ----------
        k : int
            更新箇所
    __all_apply(self, k, f)
        __d[k]に写像fを反映させ、
        要素kが葉でないとき__lz[k]を初期化する。
        Parameters
        ----------
        k : int
            更新箇所
        f : F
    __push(self, k)
        __lz[k]を子に引き継ぎ、__lz[k]を初期化する。
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
            0 <= p < self.__n
            置き換える要素の番号。
        x : S
    get(self, p)
        p番目の要素の取得
        その際、関連する遅延要素の反映を行う。
        Parameters
        ----------
        p : int
            0 <= p < self.__n
            置き換える要素の番号。
        Returns
        -------
        S
            self.__d[p]
    prod(self, l, r)
        l番目～r-1番目の要素の演算結果
        Parameters
        ----------
        l : int
        r : int
            0 <= l <= r < self.__n
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
            0 <= p < self.__n
            写像を反映させる要素の番号
        f : F
            反映させたい写像
    apply_lr(self, l, r, f)
        ※本家ではapply関数にまとめているが、引数の数が異なるため本実装では分割
        l番目～r-1番目の要素に写像fを区間反映させる。
        （遅延要素として積み込む）
        Parameters
        ----------
        l : int
        r : int
            0 <= l <= r < self.__n
        f : F
            反映させたい写像
    max_right(self, l, g)
        セグメントツリー上での二分探索結果を返却します。
        lから始めて、右側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        l : int
            0 <= l <= self.__n
            左側探索基準点
        g : function(S) -> bool
            g(e()) == Trueを満たす
        Returns
        -------
        int
            gが単調だとすれば、
            g(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最大のr
    min_left(self, r, g)
        セグメントツリー上での二分探索結果を返却します。
        rから始めて、←側に探索していく場合です。
        ※詳細は公式ドキュメント参照
        Parameters
        ----------
        r : int
            0 <= r <= self.__n
            →側探索基準点
        g : function(S) -> bool
            g(e()) == Trueを満たす
        Returns
        -------
        int
            gが単調だとすれば、
            g(op(a[l], a[l + 1], ..., a[r - 1])) = true となる最小のl
    '''
    def __init__(self, op, e, mapping, composition, id, n=0, v=[]):
        assert (len(v) >= 0) & (n >= 0)
        if len(v) == 0:
            v = [e() for _ in range(n)]
        self.__n = len(v)
        self.__log = (self.__n - 1).bit_length()
        self.__size = 1 << self.__log
        self.__d = [e() for _ in range(2 * self.__size)]
        self.__lz = [id() for _ in range(self.__size)]
        self.__op = op
        self.__e = e
        self.__mapping = mapping
        self.__composition = composition
        self.__id = id

        for i in range(self.__n):
            self.__d[self.__size + i] = v[i]
        for i in range(self.__size - 1, 0, -1):
            self.__update(i)

    def __update(self, k):
        self.__d[k] = self.__op(self.__d[2 * k], self.__d[2 * k + 1])

    def __all_apply(self, k, f):
        self.__d[k] = self.__mapping(f, self.__d[k])
        if k < self.__size:
            self.__lz[k] = self.__composition(f, self.__lz[k])

    def __push(self, k):
        self.__all_apply(2*k, self.__lz[k])
        self.__all_apply(2*k+1, self.__lz[k])
        self.__lz[k] = self.__id()

    def set(self, p, x):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        self.__d[p] = x
        for i in range(1, self.__log + 1):
            self.__update(p >> i)

    def get(self, p):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        return self.__d[p]

    def prod(self, l, r):
        assert (0 <= l) & (l <= r) & (r <= self.__n)
        if l == r:
            return self.__e()

        l += self.__size
        r += self.__size

        for i in range(self.__log, 0, -1):
            if((l >> i) << i) != l:
                self.__push(l >> i)
            if((r >> i) << i) != r:
                self.__push(r >> i)

        sml = self.__e()
        smr = self.__e()
        while l < r:
            if l & 1:
                sml = self.__op(sml, self.__d[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.__op(self.__d[r], smr)
            l //= 2
            r //= 2

        return self.__op(sml, smr)

    def all_prod(self):
        return self.__d[1]

    def apply(self, p, f):
        assert (0 <= p) & (p < self.__n)
        p += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(p >> i)
        self.__d[p] = self.__mapping(f, self.__d[p])
        for i in range(1, self.__log+1):
            self.__update(p >> i)

    def apply_lr(self, l, r, f):
        assert (0 <= l) & (l <= r) & (r <= self.__n)
        if l == r:
            return

        l += self.__size
        r += self.__size

        for i in range(self.__log, 0, -1):
            if((l >> i) << i) != l:
                self.__push(l >> i)
            if((r >> i) << i) != r:
                self.__push((r-1) >> i)

        l2, r2 = l, r
        while l < r:
            if l & 1:
                self.__all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self.__all_apply(r, f)
            l //= 2
            r //= 2
        l, r = l2, r2

        for i in range(1, self.__log+1):
            if((l >> i) << i) != l:
                self.__update(l >> i)
            if((r >> i) << i) != r:
                self.__update((r-1) >> i)

    def max_right(self, l, g):
        assert (0 <= l) & (l <= self.__n)
        assert g(self.__e())
        if l == self.__n:
            return self.__n
        l += self.__size
        for i in range(self.__log, 0, -1):
            self.__push(l >> i)
        sm = self.__e()
        while True:
            while(l % 2 == 0):
                l //= 2
            if not g(self.__op(sm, self.__d[l])):
                while l < self.__size:
                    self.__push(l)
                    l *= 2
                    if g(self.__op(sm, self.__d[l])):
                        sm = self.__op(sm, self.__d[l])
                        l += 1
                return l - self.__size
            sm = self.__op(sm, self.__d[l])
            l += 1
            if(l & -l) == l:
                break
        return self.__n

    def min_left(self, r, g):
        assert (0 <= r) & (r <= self.__n)
        assert g(self.__e())
        if r == 0:
            return 0
        r += self.__size
        for i in range(self.__log, 0, -1):
            self.__push((r-1) >> i)
        sm = self.__e()
        while True:
            r -= 1
            while(r > 1) & (r % 2):
                r //= 2
            if not g(self.__op(self.__d[r], sm)):
                while r < self.__size:
                    self.__push(r)
                    r = 2 * r + 1
                    if g(self.__op(self.__d[r], sm)):
                        sm = self.__op(self.__d[r], sm)
                        r -= 1
                return r + 1 - self.__size
            sm = self.__op(self.__d[r], sm)
            if(r & -r) == r:
                break
        return 0
