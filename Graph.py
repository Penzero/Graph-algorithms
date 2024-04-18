import random
from GraphIterator import GraphIterator


class Graph:
    def __init__(self, reversible: bool, weighted: bool = False):
        self.__nodes = 0
        self.__reversible = reversible
        self.__weighted = weighted  # Indicates if the graph is weighted
        self.__graph = []

    def get_graph(self):
        return self.__graph

    def add_vertex(self):
        self.__nodes += 1
        for row in self.__graph:
            row.append(0)
        self.__graph.append([0] * self.__nodes)

    def add_edge(self, vertex1, vertex2, weight=1):
        if vertex1 < 0 or vertex2 < 0 or vertex1 >= self.__nodes or vertex2 >= self.__nodes:
            raise ValueError("One or both of the vertices are not in the graph")
        if not self.__weighted:
            weight = 1  # Ensures compatibility with unweighted graphs
        self.__graph[vertex1][vertex2] = weight
        if self.__reversible:
            self.__graph[vertex2][vertex1] = weight

    def remove_edge(self, vertex1, vertex2):
        self.__graph[vertex1][vertex2] = 0
        if self.__reversible:
            self.__graph[vertex2][vertex1] = 0

    def remove_vertex(self, vertex):
        if vertex < 0 or vertex >= self.__nodes:
            raise ValueError("The vertex is not in the graph")
        self.__nodes -= 1
        self.__graph.pop(vertex)
        for row in self.__graph:
            row.pop(vertex)

    def create_random(self, n, max_weight=10):
        self.__nodes = n
        self.__graph = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    weight = random.randint(1, max_weight) if self.__weighted else 1
                    self.add_edge(i, j, weight)

    def get_n(self):
        return self.__nodes

    def get_edges(self):
        edges = []
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if self.__graph[i][j] != 0:
                    edges.append((i, j, self.__graph[i][j]) if self.__weighted else (i, j))
        return edges

    def deg(self, x):
        return sum(1 for weight in self.__graph[x] if weight != 0)

    def is_edge(self, x, y):
        return self.__graph[x][y] != 0

    def outbound_edges(self, x):
        if self.__reversible:
            return "This function is only available for non-reversible graphs"
        return [(x, i, self.__graph[x][i]) for i in range(self.__nodes) if self.__graph[x][i] != 0] if self.__weighted \
            else [i for i in range(self.__nodes) if self.__graph[x][i] != 0]

    def inbound_edges(self, x):
        if self.__reversible:
            return "This function is only available for non-reversible graphs."
        return [(i, x, self.__graph[i][x]) for i in range(self.__nodes) if self.__graph[i][x] != 0] if self.__weighted \
            else [i for i in range(self.__nodes) if self.__graph[i][x] != 0]

    def copy_graph(self):
        new_graph = Graph(self.__reversible, self.__weighted)
        new_graph.__nodes = self.__nodes
        new_graph.__graph = [row[:] for row in self.__graph]
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

    @staticmethod
    def create_from_metro_file(file_content, transfer_penalty=9):
        # Instantiate the graph
        graph = Graph(reversible=True, weighted=True)
        station_to_vertex = {}  # Maps station names to vertex indices
        vertex_to_station = {}  # Maps vertex indices to station names

        lines = file_content.strip().split('\n')
        for line in lines:
            parts = line.split(',')
            metro_line = parts[0]
            stations = parts[1:]

            last_station = None
            total_time = 0  # Accumulated time from the start of the line

            for station_info in stations:
                station_name, travel_time = station_info.strip('()').split(';')
                travel_time = int(travel_time)

                # Create or retrieve the vertex for the station
                if station_name not in station_to_vertex:
                    station_to_vertex[station_name] = len(station_to_vertex)
                    vertex_to_station[len(station_to_vertex)] = station_name
                    graph.add_vertex()

                current_vertex = station_to_vertex[station_name]

                # Add edge from the last station to the current one
                if last_station is not None:
                    graph.add_edge(station_to_vertex[last_station], current_vertex, total_time)

                # Update for the next iteration
                last_station = station_name
                total_time = travel_time

            # Adding transfer penalty edges for stations present on multiple lines
            for station in stations:
                station_name = station.strip('()').split(';')[0]
                for other_station, vertex_id in station_to_vertex.items():
                    if other_station != station_name:
                        if not graph.is_edge(vertex_id, station_to_vertex[station_name]):
                            # Add the transfer penalty edge
                            graph.add_edge(vertex_id, station_to_vertex[station_name], transfer_penalty)

        return graph, station_to_vertex, vertex_to_station

    def __str__(self):
        graph_str = ""
        for i in range(self.__nodes):
            for j in range(self.__nodes):
                if self.__graph[i][j] != 0:
                    weight_str = f" Weight: {self.__graph[i][j]}" if self.__weighted else ""
                    graph_str += f"Edge: {i} -> {j}{weight_str}\n"
        return graph_str.strip()

    def __repr__(self):
        return self.__str__()
