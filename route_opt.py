import heapq

def shortest_route(nodes, edges, source, target):
    adj = {n: [] for n in nodes}
    for a,b,c in edges:
        adj[a].append((b,c))
    dist = {n: float('inf') for n in nodes}
    dist[source] = 0
    pq = [(0,source)]
    while pq:
        d,u = heapq.heappop(pq)
        if d>dist[u]:
            continue
        if u==target:
            return dist[target]
        for v,w in adj.get(u,[]):
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                heapq.heappush(pq,(nd,v))
    return None if dist[target]==float('inf') else dist[target]
