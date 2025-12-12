import unittest
from route_opt import shortest_route

class TestRoutes(unittest.TestCase):
    def test_simple_path(self):
        nodes = ['A','B','C']
        edges = [('A','B',2),('B','C',3)]
        self.assertEqual(shortest_route(nodes, edges, 'A','C'), 5)
    def test_choose_shorter_via_node(self):
        nodes = ['A','B','C']
        edges = [('A','C',10),('A','B',3),('B','C',4)]
        self.assertEqual(shortest_route(nodes, edges, 'A','C'), 7)
    def test_unreachable(self):
        nodes = ['A','B','C']
        edges = [('A','B',1)]
        self.assertIsNone(shortest_route(nodes, edges, 'A','C'))

if __name__ == '__main__':
    unittest.main()
