import graph as g

# https://www.educative.io/collection/page/6151088528949248/4547996664463360/5698321848991744


def helperFunction(myGraph, currentNode, visited, result):
    visited[currentNode] = True  # Mark the current node as visited

    # Recur for all the adjacent vertices of currentNode
    for i in myGraph.graph[currentNode]:
        if visited[i] == False:
            helperFunction(myGraph, i, visited, result)

    result.insert(0, currentNode)  # Push current vertex to result


def topologicalSort(myGraph):
    visited = [False] * myGraph.vertices  # Mark all the vertices as not visited
    result = []  # Our stack to store the result/output

    for currentNode in range(myGraph.vertices):
        if visited[currentNode] == False:
            helperFunction(myGraph, currentNode, visited, result)

    return result


# Driver code
# Create a graph given in the above diagram
myGraph = g.Graph(5)
myGraph.addEdge(0, 1)
myGraph.addEdge(0, 3)
myGraph.addEdge(1, 2)
myGraph.addEdge(2, 3)
myGraph.addEdge(2, 4)
myGraph.addEdge(3, 4)

print("Topological Sort")
print(topologicalSort(myGraph))


import string

an = {}
na = {}

for i, s in enumerate(string.ascii_lowercase):
    na[i] = s
    an[s] = i


myGraph = g.Graph(6)
myGraph.addEdge(an["a"], an["b"])
myGraph.addEdge(an["a"], an["c"])
myGraph.addEdge(an["a"], an["d"])
myGraph.addEdge(an["a"], an["e"])
myGraph.addEdge(an["a"], an["f"])

myGraph.addEdge(an["b"], an["c"])
myGraph.addEdge(an["b"], an["f"])

myGraph.addEdge(an["c"], an["d"])

myGraph.addEdge(an["e"], an["d"])
myGraph.addEdge(an["e"], an["f"])

print("Topological Sort")
out = topologicalSort(myGraph)
out = [na[num] for num in out]
print(out)
