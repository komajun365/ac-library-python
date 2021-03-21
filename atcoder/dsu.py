class DSU:
    '''
    Union-Find木を構築する。

    Parameters
    ----------
    n : int
        要素数

    Attributes
    ----------
    _n : int
        要素数
    _parent_or_size : list
        根のインデックス、あるいは素集合のsizeの-1倍を要素に持つ

    Methods
    -------
    __init__(self, n)
        初期化

    merge(self, a, b)
        木を結合する
        Parameters
        ----------
        a, b : int
            結合対象の要素
        Returns
        -------
        x : int
            新たな代表元

    same(self, a, b)
        同じ集合に属するか判定する
        Parameters
        ----------
        a, b : int
            判定対象の要素
        Returns
        -------
        bool
            同じ集合であればTrue

    leader(self, a)
        根を返却する
        Parameters
        ----------
        a : int
            根の探索元
        Returns
        -------
        int
            aが属する集合の代表元

    size(self, a)
        素集合の要素数を返却する
        Parameters
        ----------
        a : int
            対象の要素
        Returns
        -------
        int
            aが属する集合の大きさ

    groups(self)
        すべての素集合を要素に持つリスト(二重リスト)を返却する
        Returns
        -------
        list
            素集合を枚挙したリスト(「intを要素に持つリスト」のリスト)
    '''

    def __init__(self, n):
        self._n = n
        self._parent_or_size = [-1] * n

    def merge(self, a, b):
        assert 0 <= a < self._n, "引数の値が要素数未満ではありません。"
        assert 0 <= b < self._n, "引数の値が要素数未満ではありません。"

        x, y = self.leader(a), self.leader(b)

        if x == y:
            return x

        # 小さいグループを大きなグループにmergeするため
        if -self._parent_or_size[x] < -self._parent_or_size[y]:
            x, y = y, x

        self._parent_or_size[x] += self._parent_or_size[y]
        self._parent_or_size[y] = x  # 小さいグループのリーダーのリーダーを設定

        return x

    def same(self, a, b):
        assert 0 <= a < self._n, "引数の値が要素数未満ではありません。"
        assert 0 <= b < self._n, "引数の値が要素数未満ではありません。"

        return self.leader(a) == self.leader(b)

    def leader(self, a):
        assert 0 <= a < self._n, "引数の値が要素数未満ではありません。"

        if self._parent_or_size[a] < 0:
            return a

        # 直接returnせず、リーダーの情報を更新
        self._parent_or_size[a] = self.leader(self._parent_or_size[a])

        return self._parent_or_size[a]

    def size(self, a):
        assert 0 <= a < self._n, "引数の値が要素数未満ではありません。"

        return -self._parent_or_size[self.leader(a)]

    def groups(self):
        leader_ls = [self.leader(i) for i in range(self._n)]

        result = [[] for _ in range(self._n)]
        for i in range(self._n):
            result[leader_ls[i]].append(i)

        return [e for e in result if e]  # 空リストを除く
