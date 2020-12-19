class MaxFlow:
    """
    最大フロー問題
    https://atcoder.github.io/ac-library/production/document_ja/maxflow.html
    dinic法の実装。
    本家ACLは再帰を用いて実装されているが、pypy向けに非再帰に変更。

    Parameters
    ----------
    n : int
        グラフの頂点数

    Attributes
    ----------
    _INF = 9_223_372_036_854_775_807 : int
        明に指定しなかった場合のフローの最大値
        longlong型の上限
    _n : int
        グラフの頂点数
    _pos : list[int, int]
        _pos[i]はi番目に追加した有向辺の情報を表す。
        _pos[i][0]が始点の頂点番号
        _pos[i][1]が_pos[i][0]が始点の辺のうち、何番目に追加されたかを表し、
        _g[_pos[i][0]][_pos[i][1]]で辺の情報にアクセスできる
    _g : list[ list[int, int, int] * _n]
        _g[i][j]に頂点iを始点とするj番目の辺の情報が格納されている。
        _g[i][j][0]が有向辺の終点
        _g[i][j][1]が今見ている辺の逆辺のid
        ->　逆辺の情報は_g[_g[i][j][0]][_g[i][j][1]]でアクセスできる
        _g[i][j][2]が現時点から追加して流すことのできるフローの値（余っている容量）

    Methods
    -------
    __init__(self, n=0)
        初期化
    add_edge(self, from_, to, cap)
        グラフに始点from_,終点to,容量capの辺を追加する。
        （合わせて容量0の逆辺も追加する。）
        Parameters
        ----------
        from_ : int
            0 <= from_ < self._n
        to : int
            0 <= to < self._n
        cap : int
            0 <= cap
        Returns
        -------
        int
            何番目に追加した辺であるか、を返却する。
    get_edge(self, i)
        i番目に追加した辺の情報を返却する。
        Parameters
        ----------
        i : int
            0 <= i < len(self._pos)
        Returns
        -------
        [from_, to, cap, flow] : list
            from_ : 始点の頂点番号
            to : 終点の頂点番号
            cap : 辺の容量
            flow : 現在の流量
    edges(self)
        全ての辺の情報を返却する。
        Returns
        -------
        result : list
            [[from_, to, cap, flow] for _ in range(len(self._pos)]の形式
    change_edge(self, i, new_cap, new_flow)
        i番目の辺について、容量をnew_cap,流量をnew_flowに変更する。
        逆辺以外の辺はそのまま。
        Parameters
        ----------
        i : int
            0 <= i < len(self._pos)
        new_cap : int
        new_flow : int
            0 <= new_flow <= new_cap
    _flow_bfs(self, s, t)
        関数flow内部で実施するbfs
        sを根としてtにたどり着くまでbfsを行い、
        深さの情報levelsを返却する。
        Parameters
        ----------
        s : int
            フローの始点を表す頂点番号
        t : int
            フローの終点を表す頂点番号
        Returns
        -------
        levels : list
            levels[i]がsを根とした際の頂点iの深さ
            tと同じかそれより深い頂点には興味がないため、
            tよりも前に到達できなかった頂点の深さは初期値-1のまま
    flow(self, s, t, flow_limit=_INF)
        現在の状況から新たに追加する形で、
        頂点sから頂点tまでflow_limitを超えない様にフローを流せるか試行する。
        （各辺の流量を更新する。）
        それ以上流せなくなるか、flow_limitに達した時点で終了し、
        新たに流すことのできた流量flowを返却する。
        Parameters
        ----------
        s : int
            0 <= s < self._n
            フローの始点を表す頂点番号
        t : int
            0 <= t < self._n
            s != t
            フローの終点を表す頂点番号
        flow_limit : int
            新たに流したい流量の上限
            形式的に値が必要なため_INFを初期値としているが、
            _INF以上の値を指定することも可能。
        Returns
        -------
        flow : int
            新たに流すことのできた流量
    min_cut(self, s)
        残余グラフを張ったときに、sから到達可能な頂点のリストを返却する。
        flow(s, t)をflow_limitなしでちょうど一回呼んだ後に呼ぶと、
        返り値は s,t 間のmincutに対応する。
        Parameters
        ----------
        s : int
            0 <= s < self._n
            フローの始点を表す頂点番号
        Returns
        -------
        visited : list
            visited[i]==Trueならば、i番目の頂点は残余グラフ上でsから到達可能。
    """
    _INF = 9_223_372_036_854_775_807

    def __init__(self, n=0):
        self._n = n
        self._pos = []
        self._g = [[] for _ in range(n)]  # [to, rev, cap]

    def add_edge(self, from_, to, cap):
        assert 0 <= from_ < self._n
        assert 0 <= to < self._n
        assert 0 <= cap
        m = len(self._pos)
        from_id = len(self._g[from_])
        self._pos.append([from_, from_id])
        to_id = len(self._g[to])
        if from_ == to:
            to_id += 1
        self._g[from_].append([to, to_id, cap])
        self._g[to].append([from_, from_id, 0])
        return m

    def get_edge(self, i):
        m = len(self._pos)
        assert 0 <= i < m
        _e = self._g[self._pos[i][0]][self._pos[i][1]]
        _re = self._g[_e[0]][_e[1]]
        return [self._pos[i][0], _e[0], _e[2] + _re[2], _re[2]]

    def edges(self):
        m = len(self._pos)
        result = [self.get_edge(i) for i in range(m)]
        return result

    def change_edge(self, i, new_cap, new_flow):
        m = len(self._pos)
        assert 0 <= i < m
        assert 0 <= new_flow <= new_cap
        _e = self._g[self._pos[i][0]][self._pos[i][1]]
        _re = self._g[_e[0]][_e[1]]
        _e[2] = new_cap - new_flow
        _re[2] = new_flow

    def _flow_bfs(self, s, t):
        level = [-1] * self._n
        level[s] = 0
        que = [s]
        while que:
            next_que = []
            for v in que:
                for to, rev, cap in self._g[v]:
                    if cap == 0 or level[to] >= 0:
                        continue
                    level[to] = level[v] + 1
                    if to == t:
                        return level
                    next_que.append(to)
            que, next_que = next_que, que
        return level

    def flow(self, s, t, flow_limit=_INF):
        assert 0 <= s < self._n
        assert 0 <= t < self._n
        assert s != t

        flow = 0
        while flow < flow_limit:
            level = self._flow_bfs(s, t)
            if level[t] == -1:
                break

            iterator = [0] * self._n
            in_ = [0] * self._n
            out = [0] * self._n

            in_[t] = flow_limit - flow
            route = [t]
            while route:
                v = route[-1]
                if in_[v] == out[v] and v == t:
                    flow += out[t]
                    return flow
                if v == s or in_[v] == out[v]:
                    route.pop()
                    w = route[-1]
                    flow_vw = in_[v]
                    i = iterator[w]
                    to, rev, cap = self._g[w][i]
                    self._g[v][rev][2] -= flow_vw
                    self._g[w][i][2] += flow_vw
                    out[w] += flow_vw
                    continue

                for i in range(iterator[v], len(self._g[v])):
                    to, rev, cap = self._g[v][i]
                    if(level[to] == -1
                       or level[v] <= level[to]
                       or self._g[to][rev][2] == 0):
                        continue
                    in_[to] = min(in_[v]-out[v], self._g[to][rev][2])
                    out[to] = 0
                    route.append(to)
                    iterator[v] = i
                    break
                else:
                    iterator[v] = len(self._g[v])
                    route.pop()
                    if v == t:
                        if out[t] == 0:
                            return flow
                        flow += out[t]
                        continue
                    w = route[-1]
                    flow_vw = out[v]
                    i = iterator[w]
                    to, rev, cap = self._g[w][i]
                    self._g[v][rev][2] -= flow_vw
                    self._g[w][i][2] += flow_vw
                    out[w] += flow_vw
                    iterator[w] += 1
        return flow

    def min_cut(self, s):
        visited = [False] * self._n
        visited[s] = True
        que = [s]
        while que:
            next_que = []
            for p in que:
                for to, rev, cap in self._g[p]:
                    if cap > 0 and not visited[to]:
                        visited[to] = True
                        next_que.append(to)
            que, next_que = next_que, que
        return visited
