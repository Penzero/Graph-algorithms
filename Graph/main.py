from Graph import Graph
from Metro import Metro


def postorder_traversal(root):
    if not root:
        return []
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.value]


def print_menu(graph):
    print("Graph type: " + ("Undirected" if graph.is_reversible() else "Directed") +
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
    print("12. Check if graph is DAG")
    print("13. Topological sort")
    print("14. Count distinct paths between two vertices")
    print("15. Reconstruct tree from traversals")
    print("16. Check if graph is Eulerian")
    print("17. Find Eulerian circuit")
    print("0. Exit")

if __name__ == "__main__":
    command = input("Choose what graph do you want to use (Graph/Metro): ")
    if command == "Graph":
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
                    directed = input("Is the graph directed? (yes/no): ").strip().lower() == 'yes'
                    weighted = input("Is the graph weighted? (yes/no): ").strip().lower() == 'yes'
                    graph.create_random(n, directed=directed, weighted=weighted)
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
                elif command == "12":
                    if graph.is_dag():
                        print("The graph is a DAG.")
                    else:
                        print("The graph is not a DAG.")
                elif command == "13":
                    if graph.is_dag():
                        print("Topological Sort: ", graph.topological_sort())
                    else:
                        print("The graph is not a DAG, cannot perform topological sort.")
                elif command == "14":
                    start_vertex = int(input("Enter start vertex: "))
                    end_vertex = int(input("Enter end vertex: "))
                    if graph.is_dag():
                        print(f"Number of distinct paths from {start_vertex} to {end_vertex}: {graph.count_paths(start_vertex, end_vertex)}")
                    else:
                        print("The graph is not a DAG, cannot count distinct paths.")
                elif command == "15":
                    inorder = list(map(int, input("Enter inorder traversal (space-separated): ").split()))
                    preorder = list(map(int, input("Enter preorder traversal (space-separated): ").split()))
                    postorder = list(map(int, input("Enter postorder traversal (space-separated): ").split()))
                    tree_root = graph.build_tree_from_inorder_preorder(inorder, preorder)
                    graph.add_tree_edges(tree_root)
                    print("Tree constructed and added to the graph.")
                    graph.print_tree(tree_root)
                    reconstructed_postorder = postorder_traversal(tree_root)
                    print("Reconstructed Postorder:", reconstructed_postorder)
                    print("Original Postorder:", postorder)
                    print("Match:", reconstructed_postorder == postorder)
                elif command == "16":
                    if graph.is_eulerian():
                        print("The graph is Eulerian.")
                    else:
                        print("The graph is not Eulerian.")
                elif command == "17":
                    if graph.is_eulerian():
                        circuit = graph.find_eulerian_circuit()
                        print("Eulerian Circuit:", circuit)
                    else:
                        print("The graph is not Eulerian.")
                elif command == "0":
                    break
                else:
                    print("Invalid command")

                inp = input("Do you want to continue? (y/n): ")
                if inp == 'n':
                    break
                print()

            except Exception as e:
                print(e)
                print()

    elif command == "Metro":
        metro = Metro()
        metro.create_metro_from_file("input.txt")

        while True:
            try:
                print("1. Shortest path")
                print("2. Exit")
                command = input("Enter command: ")

                if command == "1":
                    start_station = input("Enter starting station: ")
                    metro.dijkstra(start_station)
                elif command == "2":
                    break
                else:
                    print("Invalid command")

            except Exception as e:
                print(e)
                print()



