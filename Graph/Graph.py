from GraphIterator import GraphIterator
import random


class TreeNode:
    def __init__(self, value=0):
        self.value = value
        self.left = None
        self.right = None


class Graph:
    def __init__(self, reversible: bool, weighted: bool):
        self.__nodes = 0
        self.__reversible = reversible
        self.__weighted = weighted
        self._graph = []

    def get_graph(self):
        return self._graph

    def add_vertex(self):
        self.__nodes += 1
        for row in self._graph:
            row.append(0)
        self._graph.append([0] * self.__nodes)
        return self.__nodes - 1

    def add_edge(self, vertex1, vertex2, weight=1):
        if vertex1 < 0 or vertex2 < 0 or vertex1 >= self.__nodes or vertex2 >= self.__nodes:
            raise ValueError("One or both of the vertices are not in the graph")
        if not self.__weighted:
            weight = 1  # Ensures compatibility with unweighted graphs
        self._graph[vertex1][vertex2] = weight
        if self.__reversible:
            self._graph[vertex2][vertex1] = weight

    def remove_edge(self, vertex1, vertex2):
        self._graph[vertex1][vertex2] = 0
        if self.__reversible:
            self._graph[vertex2][vertex1] = 0

    def remove_vertex(self, vertex):
        if vertex < 0 or vertex >= self.__nodes:
            raise ValueError("The vertex is not in the graph")
        self.__nodes -= 1
        self._graph.pop(vertex)
        for row in self._graph:
            row.pop(vertex)

    def create_random(self, n, max_weight=10, directed=True, weighted=True):
        self.__nodes = n
        self.__reversible = directed
        self.__weighted = weighted
        self._graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j and random.random() < 0.5:
                    weight = random.randint(1, max_weight) if self.__weighted else 1
                    self.add_edge(i, j, weight)
                    if not directed:
                        self.add_edge(j, i, weight)

    def get_n(self):
        return self.__nodes

    def get_edges(self):
        edges = []
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if self._graph[i][j] != 0:
                    edges.append((i, j, self._graph[i][j]) if self.__weighted else (i, j))
        return edges

    def deg(self, x):
        return sum(1 for weight in self._graph[x] if weight != 0)+sum(1 for weight in self._graph if weight[x] != 0)

    def is_edge(self, x, y):
        return self._graph[x][y] != 0

    def outbound_edges(self, x):
        if self.__reversible:
            return "This function is only available for non-reversible graphs"
        return [(x, i, self._graph[x][i]) for i in range(self.__nodes) if self._graph[x][i] != 0] if self.__weighted \
            else [i for i in range(self.__nodes) if self._graph[x][i] != 0]

    def inbound_edges(self, x):
        if self.__reversible:
            return "This function is only available for non-reversible graphs."
        return [(i, x, self._graph[i][x]) for i in range(self.__nodes) if self._graph[i][x] != 0] if self.__weighted \
            else [i for i in range(self.__nodes) if self._graph[i][x] != 0]

    def copy_graph(self):
        new_graph = Graph(self.__reversible, self.__weighted)
        new_graph.__nodes = self.__nodes
        new_graph._graph = [row[:] for row in self._graph]
        return new_graph

    def is_reversible(self):
        return self.__reversible

    def iter_vertex(self, start_vertex):
        return GraphIterator(self, start_vertex)

    def is_weighted(self):
        return self.__weighted

    @staticmethod
    def create_from_file(file_name):
        with open(file_name, "r") as file:
            n, m, reversible, weighted = file.readline().strip().split()
            n, m = int(n), int(m)
            reversible = True if reversible == "T" else False
            weighted = True if weighted == "T" else False

            graph = Graph(reversible, weighted)

            for _ in range(n):
                graph.add_vertex()

            for _ in range(m):
                edge_data = file.readline().strip().split()
                if weighted:
                    vertex1, vertex2, weight = int(edge_data[0]), int(edge_data[1]), int(edge_data[2])
                    graph.add_edge(vertex1, vertex2, weight)
                else:
                    vertex1, vertex2 = int(edge_data[0]), int(edge_data[1])
                    graph.add_edge(vertex1, vertex2)

            return graph

    def __str__(self):
        graph_str = ""
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if self._graph[i][j] != 0:
                    weight_str = f" Weight: {self._graph[i][j]}" if self.__weighted else ""
                    graph_str += f"Edge: {i} -> {j}{weight_str}\n"
        return graph_str.strip()

    def __repr__(self):
        return self.__str__()

    def is_dag(self):
        """Check if the graph is a DAG using DFS."""
        visited = [False] * self.__nodes
        rec_stack = [False] * self.__nodes

        def dfs(v):
            visited[v] = True
            rec_stack[v] = True

            for i in range(self.__nodes):
                if self._graph[v][i] != 0:
                    if not visited[i]:
                        if dfs(i):
                            return True
                    elif rec_stack[i]:
                        return True

            rec_stack[v] = False
            return False

        for node in range(self.__nodes):
            if not visited[node]:
                if dfs(node):
                    return False
        return True

    def topological_sort(self):
        """Perform topological sort on the graph."""
        visited = [False] * self.__nodes
        stack = []

        def dfs(v):
            visited[v] = True
            for i in range(self.__nodes):
                if self._graph[v][i] != 0 and not visited[i]:
                    dfs(i)
            stack.append(v)

        for i in range(self.__nodes):
            if not visited[i]:
                dfs(i)

        stack.reverse()
        return stack

    def count_paths(self, start, end):
        """Count the number of distinct paths from start to end in a DAG."""
        if not self.is_dag():
            return "The graph is not a DAG."

        top_order = self.topological_sort()
        paths = [0] * self.__nodes
        paths[start] = 1

        for node in top_order:
            if paths[node] != 0:
                for i in range(self.__nodes):
                    if self._graph[node][i] != 0:
                        paths[i] += paths[node]

        return paths[end]

    def build_tree_from_inorder_preorder(self, inorder, preorder):
        if not inorder or not preorder:
            return None

        # Helper function to construct the binary tree
        def build_tree(inorder_map, start, end):
            if start > end:
                return None

            # The first element in preorder is the root
            root_value = preorder.pop(0)
            root_index = inorder_map[root_value]
            root = TreeNode(root_value)

            # Build left and right subtrees recursively
            root.left = build_tree(inorder_map, start, root_index - 1)
            root.right = build_tree(inorder_map, root_index + 1, end)

            return root

        # Map each value to its index in inorder for O(1) access
        inorder_map = {value: idx for idx, value in enumerate(inorder)}
        return build_tree(inorder_map, 0, len(inorder) - 1)

    def add_tree_edges(self, root):
        if not root:
            return

        def add_edges(node):
            if node.left:
                left_index = self.add_vertex()
                self.add_edge(node.value, left_index)
                add_edges(node.left)

            if node.right:
                right_index = self.add_vertex()
                self.add_edge(node.value, right_index)
                add_edges(node.right)

        root_index = self.add_vertex()
        self.add_edge(root.value, root_index)
        add_edges(root)

    def print_tree(self, root, depth=0, label="Root:"):
        if not root:
            return
        print(" " * (depth * 2) + label + str(root.value))
        self.print_tree(root.left, depth + 1, "L---")
        self.print_tree(root.right, depth + 1, "R---")

    def is_eulerian(self):
        """Check if the graph is Eulerian."""
        if not self.__is_connected():
            print("The graph is not connected.")
            return False

        for i in range(self.__nodes):
            if self.deg(i) % 2 != 0:
                print(f"Vertex {i} has an odd degree.")
                return False

        return True

    def __is_connected(self):
        """Check if the graph is connected."""
        visited = [False] * self.__nodes

        def dfs(v):
            visited[v] = True
            for i in range(self.__nodes):
                if self._graph[v][i] != 0 and not visited[i]:
                    dfs(i)

        # Find a vertex with a non-zero degree
        start_vertex = next((i for i in range(self.__nodes) if self.deg(i) > 0), None)
        if start_vertex is None:
            return True

        # Perform DFS from the found vertex
        dfs(start_vertex)

        # Check if all vertices with non-zero degree are connected
        return all(visited[i] or self.deg(i) == 0 for i in range(self.__nodes))

    def find_eulerian_circuit(self):
        """Find an Eulerian circuit using Hierholzer's algorithm."""
        if not self.is_eulerian():
            return "The graph is not Eulerian."

        graph_copy = self.copy_graph()
        circuit = []
        current_path = []

        # Start from any vertex with an edge
        current_vertex = next((i for i in range(self.__nodes) if self.deg(i) > 0), None)
        if current_vertex is None:
            return circuit

        current_path.append(current_vertex)

        while current_path:
            if any(graph_copy._graph[current_vertex]):
                next_vertex = graph_copy._graph[current_vertex].index(
                    next(filter(lambda x: x > 0, graph_copy._graph[current_vertex])))
                current_path.append(current_vertex)
                graph_copy.remove_edge(current_vertex, next_vertex)
                current_vertex = next_vertex
            else:
                circuit.append(current_vertex)
                current_vertex = current_path.pop()

        circuit.reverse()
        return circuit

