class InternalScc():
    def __init__(self, n=0):
        self._n = n
        self.edges = [] # [int, edge]
        
    def num_vertices(self):
        return self._n
    
    def add_edge(self, from_, to):
        self.edges.append([from_, [to]])