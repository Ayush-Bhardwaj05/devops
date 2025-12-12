from route_opt import shortest_route
nodes = ['A','B','C','D']
edges = [('A','B',5),('B','C',4),('A','C',10),('C','D',3)]
res = shortest_route(nodes, edges, 'A','D')
print(f"shortest A->D = {res}")
