class Csr():
    """
    グラフの辺の情報を格納するデータ型。
    CSR：Compressed Sparse Row　だが、ScipyなどのCSRの実装とは異なる。
    // Reference:
    // R. Tarjan,
    // Depth-First Search and Linear Graph Algorithms

    Parameters
    ----------
    n : int
        グラフの頂点数
    edges : list[x : int, e : list]
        グラフの辺の情報
        xは属する点の情報（有向辺のfromに当たる点の番号）
        eは辺の情報（長さ・情報は可変）

    Attributes
    ----------
    start : list
    elist : list
        点i(0-indexed)に紐づく辺の情報はelist[start[i]:start[i+1]]に格納される。
        elistに持たせる情報は可変。（隣接点だけ、隣接点＋コスト、など）
    """
    def __init__(self, n: int, edges: list):
        self.start = [0] * (n + 1)
        self.elist = [0] * len(edges)
        for e in edges:
            self.start[e[0] + 1] += 1
        for i in range(1, n + 1):
            self.start[i] += self.start[i - 1]
        counter = self.start[::]
        for e in edges:
            self.elist[counter[e[0]]] = e[1]
            counter[e[0]] += 1
