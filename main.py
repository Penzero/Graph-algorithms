from Graph import Graph


def print_menu(graph):
    print("Graph type: " + ("Directed" if graph.is_reversible() else "Undirected") +
          ", " + ("Weighted" if graph.is_weighted() else "Unweighted"))
    print("1. Add vertex")
    print("2. Add edge")
    print("3. Remove vertex")
    print("4. Remove edge")
    print("5. Create random graph")
    print("6. Get degree of vertex")
    print("7. Check if there is an edge between two vertices")
    print("8. Copy graph")
    print("9. Display graph")
    print("10. Depth-first search")
    print("11. Get path length")
    print("0. Exit")


if __name__ == "__main__":
    graph = Graph.create_from_file("graph.txt")
    while True:
        try:
            print_menu(graph)
            command = input("Enter command: ")
            if command == "1":
                graph.add_vertex()
                print(graph)
                print()
                print("Vertex added.")
            elif command == "2":
                vertex1 = int(input("Enter first vertex: "))
                vertex2 = int(input("Enter second vertex: "))
                if graph.is_weighted():
                    weight = float(input("Enter weight: "))
                    graph.add_edge(vertex1, vertex2, weight)
                else:
                    graph.add_edge(vertex1, vertex2)
                print(graph)
                print()
                print("Edge added.")
            elif command == "3":
                vertex = int(input("Enter vertex to remove: "))
                graph.remove_vertex(vertex)
                print(graph)
                print()
                print(f"Vertex {vertex} removed.")
            elif command == "4":
                vertex1 = int(input("Enter first vertex: "))
                vertex2 = int(input("Enter second vertex: "))
                graph.remove_edge(vertex1, vertex2)
                print(graph)
                print()
                print("Edge removed.")
            elif command == "5":
                n = int(input("Enter number of vertices: "))
                graph.create_random(n)
                print(graph)
                print()
                print("Random graph created.")
            elif command == "6":
                vertex = int(input("Enter vertex: "))
                print(f"Degree of vertex {vertex}: {graph.deg(vertex)}")
            elif command == "7":
                vertex1 = int(input("Enter first vertex: "))
                vertex2 = int(input("Enter second vertex: "))
                print("Edge exists: " + str(graph.is_edge(vertex1, vertex2)))
            elif command == "8":
                copy = graph.copy_graph()
                print("Graph copied.")
            elif command == "9":
                print(graph)
            elif command == "10":
                start_vertex = int(input("Enter start vertex: "))
                iterator = graph.iter_vertex(start_vertex)
                iterator.first()
                while iterator.valid():
                    print(iterator.get_current())
                    iterator.next()
            elif command == "11":
                start_vertex = int(input("Enter start vertex: "))
                iterator = graph.iter_vertex(start_vertex)
                iterator.first()
                while iterator.valid():
                    print(iterator.get_path_length())
                    iterator.next()
            elif command == "0":
                break
            else:
                print("Invalid command")
        except Exception as e:
            print(e)
            print()
