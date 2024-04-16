class GraphIterator:
    def __init__(self, graph, start_vertex):
        self.graph = graph
        self.start_vertex = start_vertex
        self.visited = set()
        self.stack = []
        self.current_vertex = None
        self.vertex_depth = {start_vertex: 0}

    def first(self):
        self.stack = [(self.start_vertex, 0)]
        self.visited = {self.start_vertex}
        self.current_vertex = None
        self.vertex_depth = {self.start_vertex: 0}
        self.next()

    def next(self):
        if not self.stack:
            self.current_vertex = None
            return
        self.current_vertex, current_depth = self.stack.pop()
        for neighbour in range(self.graph.get_n() - 1, -1, -1):
            if self.graph.is_edge(self.current_vertex, neighbour) and neighbour not in self.visited:
                self.stack.append((neighbour, current_depth + 1))
                self.visited.add(neighbour)
                self.vertex_depth[neighbour] = current_depth + 1

    def get_current(self):
        if not self.valid():
            raise ValueError("Iterator is not valid")
        return self.current_vertex

    def get_path_length(self):
        if not self.valid():
            raise ValueError("Iterator is not valid or has finished traversing")
        return self.vertex_depth[self.current_vertex]

    def valid(self):
        return self.current_vertex is not None or bool(self.stack)


