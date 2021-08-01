import numpy as np
import math
import networkx as nx


def limblength(j, mat):
    """
    get the limb length of species j
    """
    minval = math.inf

    for i in range(len(mat)):
        for k in range(len(mat[i])):
            if i != k and j != k and i != j:
                minval = min(minval, (mat[i, j] + mat[j, k] - mat[i, k]) / 2.0)

    return int(minval)


def additive_phylogency(matrix):

    max_node = len(matrix)

    def additive_helper(matrix):

        if len(matrix) == 2:
            tree = {}
            tree[(0, 1)] = matrix[0, 1]
            tree[(1, 0)] = matrix[0, 1]
            return tree

        n = len(matrix) - 1

        limblen = limblength(n, matrix)

        for j in range(len(matrix)):
            if j != n:
                matrix[j, n] -= limblen
                matrix[n, j] = matrix[j, n]

        brk = 0
        for i in range(len(matrix)):
            for k in range(len(matrix)):
                if i != k != n and matrix[i, k] == matrix[i, n] + matrix[n, k]:
                    brk = 1
                    break
            if brk == 1:
                break

        x = matrix[i, n]

        matrix = np.delete(matrix, n, 0)
        matrix = np.delete(matrix, n, 1)

        tree = additive_helper(matrix)

        v = node_at_distance(tree, i, k, x)

        tree[(v, n)] = limblen
        tree[(n, v)] = limblen

        return tree

    def node_at_distance(tree, i, k, x):
        """
        node at matrixance x from i, to k
        """
        print("node at matrix i k x", i, k, x)

        nonlocal max_node

        G = nx.Graph()
        for tup, weight in tree.items():
            G.add_edge(tup[0], tup[1], weight=weight)
        path = None

        try:
            path = nx.shortest_path(G, i, k, weight="weight")
            print("path found", path)

        except:
            tree[(max_node, i)] = x
            tree[(i, max_node)] = x
            max_node += 1
            return max_node

        wt = 0
        for i in range(1, len(path)):
            wt += tree[(path[i - 1], path[i])]
            if wt == x:
                print("node exists")
                return path[i]
            if wt > x:
                tree[(max_node, i)] = x
                tree[(i, max_node)] = x
                max_node += 1
                return max_node

    return additive_helper(matrix)


if __name__ == "__main__":

    with open("dataset_10330_6sample.txt") as f:
        data = f.read().splitlines()

    n = int(data[0])

    matrix = []
    for line in data[1:]:
        matrix.append([int(i) for i in line.split()])

    matrix = np.array(matrix)

    out = additive_phylogency(matrix)
    print(out)
