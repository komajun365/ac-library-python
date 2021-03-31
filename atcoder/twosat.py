from atcoder import InternalScc


class TwoSAT:
    """
    2-SATを解きます。
    https://atcoder.github.io/ac-library/master/document_ja/twosat.html

    Parameters
    ----------
    n : int
        変数の総数

    Attributes
    ----------
    _n : int
        変数の総数
    _answer : list[bool]
        satisfiable()実行後、
        条件を満たす割り当てが存在した場合に割り当てを格納する。
    _scc : INternalScc
        2-SAT問題を解くための内部グラフ

    Methods
    -------
    __init__(self, n=0)
        初期化
    add_clause(self, i, f, j, g)
        x_i = f もしくは x_j = g というクローズを追加する。
        Parameters
        ----------
        i : int
            0 <= i < self._n
        f : bool
        j : int
            0 <= j < self._n
        g : bool
    satisfiable(self)
        現在のクローズに対して、条件を満たす割り当てが存在するか判定する。
        また、割り当てが存在するとき_answerを更新する。
        Returns
        -------
        res : bool
            割り当てが存在すればTrue,しなければFalse
    answer(self)
        satisfiable()実行後、
        条件を満たす割り当てが存在した場合に割り当てを返却する。
        satisfiable()未実施、あるいは割り当てが存在しなかった場合の返却値は未定義。
        Returns
        -------
        _answer : list[bool]
    """
    def __init__(self, n=0):
        self._n = n
        self._answer = [0] * n
        self._scc = InternalScc(2 * n)

    def add_clause(self, i, f, j, g):
        assert 0 <= i < self._n
        assert 0 <= j < self._n
        self._scc.add_edge(2 * i + (1 - f), 2 * j + g)
        self._scc.add_edge(2 * j + (1 - g), 2 * i + f)

    def satisfiable(self):
        id = self._scc.scc_ids()[1]
        for i in range(self._n):
            if id[2 * i] == id[2 * i + 1]:
                return False
            self._answer[i] = (id[2 * i] < id[2 * i + 1])
        return True

    def answer(self):
        return self._answer
