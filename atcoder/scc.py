from atcoder import InternalScc


class Scc(InternalScc):
    """
    有向グラフの強連結成分分解
    https://atcoder.github.io/ac-library/document_ja/scc.html

    InternalSccを継承
    """

    def add_edge(self, from_, to):
        n = super().num_vertices()
        assert 0 <= from_ < n
        assert 0 <= to < n
        super().add_edge(from_, to)
