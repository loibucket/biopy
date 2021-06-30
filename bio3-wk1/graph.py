from collections import defaultdict

# https://www.educative.io/collection/page/6151088528949248/4547996664463360/5698321848991744


class Graph:

    # Constructor
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.vertices = vertices

    def addEdge(self, u, v):
        self.graph[u].append(v)
