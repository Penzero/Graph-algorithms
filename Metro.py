from Graph import Graph
import heapq


class Metro(Graph):
    def __init__(self, reversible: bool = True, weighted: bool = True):
        super().__init__(reversible, weighted)

        self.__created_nodes = 0
        self.__station_nodes = dict()
        self.__node_to_station = dict()

    def create_metro_from_file(self, file_name: str = None) -> None:
        if file_name is None:
            raise ValueError("Invalid usage: no file provided!")

        with open(file_name, 'r') as fin:
            input_lines = fin.readlines()

            for line_info in input_lines:
                stations = line_info.strip().split(',')[1:]
                last_station_node = -1

                for station_info in stations:
                    curr_station, weight = station_info.strip()[1:-1].split(';')
                    weight = int(weight)

                    if curr_station not in self.__station_nodes:
                        self.__station_nodes[curr_station] = []

                    self.__station_nodes[curr_station].append(self.__created_nodes)
                    self.__node_to_station[self.__created_nodes] = curr_station

                    self.__created_nodes += 1
                    self.add_vertex()

                    if last_station_node != -1:
                        self.add_edge(last_station_node, self.__created_nodes - 1, weight)

                    last_station_node = self.__created_nodes - 1

        for station in self.__station_nodes:
            for from_vertex in self.__station_nodes[station]:
                for to_vertex in self.__station_nodes[station]:
                    if from_vertex != to_vertex:
                        self.add_edge(from_vertex, to_vertex, 3)

    def dijkstra(self, start_station: str = None):
        if start_station is None:
            raise ValueError("Starting station was not provided!")

        if start_station not in self.__station_nodes:
            raise ValueError("Start station does not exist in the metro system.")

        # Get the total number of nodes created
        num_nodes = self.__created_nodes
        min_dist = [float('inf')] * num_nodes
        prev_node = [-1] * num_nodes
        pq = []

        # Enqueue all nodes corresponding to the start station
        start_nodes = self.__station_nodes[start_station]
        for node in start_nodes:
            min_dist[node] = 0
            heapq.heappush(pq, (0, node))

        while pq:
            current_dist, current_node = heapq.heappop(pq)

            if current_dist > min_dist[current_node]:
                continue

            # Traverse all neighboring nodes
            for neighbor in range(num_nodes):
                if self._graph[current_node][neighbor] != 0:  # There's a direct path
                    edge_weight = self._graph[current_node][neighbor]
                    if min_dist[neighbor] > current_dist + edge_weight:
                        min_dist[neighbor] = current_dist + edge_weight
                        prev_node[neighbor] = current_node
                        heapq.heappush(pq, (min_dist[neighbor], neighbor))

        # Printing or returning the paths and distances
        self.print_paths(start_station, min_dist, prev_node)

    def print_paths(self, start_station, min_dist, prev_node):
        for end_station in self.__station_nodes:
            if start_station == end_station:
                continue

            best_distance = float('inf')
            best_node = -1

            # Find the node with the least distance in the destination station's node set
            for node in self.__station_nodes[end_station]:
                if min_dist[node] < best_distance:
                    best_distance = min_dist[node]
                    best_node = node

            if best_distance == float('inf'):
                print(f"There is no path between {start_station} and {end_station}")
                continue

            # Construct the path
            path = []
            current_node = best_node
            while current_node != -1:
                current_station = self.__node_to_station[current_node]
                if not path or path[-1] != current_station:
                    path.append(current_station)
                current_node = prev_node[current_node]

            path.reverse()

            print(f"Distance from {start_station} to {end_station}: {best_distance} minutes")
            print(f"Path: {', '.join(path)}\n")

    def __str__(self):
        graph_str = "Metro Network:\n"
        nodes = self.get_n()
        for i in range(nodes):
            for j in range(nodes):
                if self._graph[i][j] != 0:
                    graph_str += f"Station {i} -> Station {j} with travel time: {self._graph[i][j]} minutes\n"
        return graph_str
