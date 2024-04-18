import unittest
from Graph import Graph


class TestGraph(unittest.TestCase):
    def test_add_vertex(self):
        g = Graph(reversible=False)
        g.add_vertex()
        self.assertEqual(g.get_n(), 1)
        self.assertEqual(len(g.get_graph()), 1)

    def test_add_edge_unweighted(self):
        g = Graph(reversible=False)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1)
        self.assertTrue(g.is_edge(0, 1))
        self.assertFalse(g.is_edge(1, 0))

    def test_add_edge_weighted(self):
        g = Graph(reversible=True, weighted=True)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1, 5)
        self.assertEqual(g.get_graph()[0][1], 5)
        self.assertEqual(g.get_graph()[1][0], 5)

    def test_remove_vertex(self):
        g = Graph(reversible=True, weighted=True)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1, 2)
        g.remove_vertex(1)
        self.assertEqual(g.get_n(), 2)
        self.assertFalse(g.is_edge(0, 1))

    def test_remove_edge(self):
        g = Graph(reversible=True)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1)
        g.remove_edge(0, 1)
        self.assertFalse(g.is_edge(0, 1))
        self.assertFalse(g.is_edge(1, 0))

    def test_graph_copy(self):
        g = Graph(reversible=False)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 2)
        g_copy = g.copy_graph()
        self.assertEqual(g.get_edges(), g_copy.get_edges())
        g.add_vertex()
        self.assertNotEqual(g.get_n(), g_copy.get_n())

    def test_create_random(self):
        g = Graph(reversible=False, weighted=True)
        g.create_random(5, max_weight=10)
        self.assertEqual(g.get_n(), 5)
        self.assertTrue(any(weight != 0 for row in g.get_graph() for weight in row))

    def test_deg(self):
        g = Graph(reversible=True)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1)
        self.assertEqual(g.deg(0), 1)
        self.assertEqual(g.deg(1), 1)

    def test_iter_vertex(self):
        g = Graph(reversible=True, weighted=False)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)
        iterator = g.iter_vertex(0)
        iterator.first()

        while iterator.valid():
            print(iterator.get_current())
            iterator.next()

    def test_get_path_length(self):
        g = Graph(reversible=True, weighted=False)
        for _ in range(3):
            g.add_vertex()
        g.add_edge(0, 1)
        g.add_edge(1, 2)
        g.add_edge(0, 2)
        iterator = g.iter_vertex(0)
        iterator.first()

        while iterator.valid():
            print(iterator.get_path_length())
            iterator.next()



if __name__ == '__main__':
    unittest.main()
