import numpy as np
import math
import networkx as nx
import matplotlib.pyplot as plt
import copy

plot_cnt = 0


def limblength(j, mat):
    """
    get the limb length of species j
    """

    minval = math.inf

    for i in range(len(mat)):
        for k in range(len(mat[i])):
            if i != j != k:
                minval = min(minval, (mat[i, j] + mat[j, k] - mat[i, k]) / 2.0)

    return int(minval)


def find_i_k(matrix, n_minus_one, limblen):
    """
    find i and k, where n_minus_one's parent node is in the path from i to k
    """
    for i, _ in enumerate(matrix):
        for k, _ in enumerate(matrix):
            if i != k != n_minus_one and matrix[i, k] == matrix[i, n_minus_one] + matrix[n_minus_one, k] - 2 * limblen:
                return i, k


def node_at_distance(G, i, k, x, weight, new_node):
    """
    return node at distance x from i, on a path between i and k
    create this node in graph G if it does not exist
    """

    paths = None
    try:
        path = nx.shortest_path(G, i, k)
    except:
        print("warning A")
        G.add_edge(i, k, weight=weight)
        path = nx.shortest_path(G, i, k)

    wtold = 0
    wt = 0
    for it in range(1, len(path)):
        wtold = wt
        wt += G[path[it - 1]][path[it]]["weight"]
        if wt == x:
            return path[it]
        elif wt > x:
            print(path, "path", path[it - 1], path[it], "weight", G[path[it - 1]][path[it]]["weight"], "new_node", new_node)

            print("a add_edge (%s,%s):%s" % (path[it - 1], new_node, x - wtold))
            G.add_edge(path[it - 1], new_node, weight=x - wtold)

            print("b add_edge (%s,%s):%s" % (new_node, path[it], wt - x))
            G.add_edge(new_node, path[it], weight=wt - x)

            print("c remove_edge (%s,%s)" % (path[it - 1], path[it]))
            G.remove_edge(path[it - 1], path[it])

            return new_node

    print("return -1")
    return -1


def additive_phylogeny(matrix, n, G):
    """
    create a phylogeny graph from a matrix of distances between n species
    store the graph in G
    """
    new_node = n

    def additive_recur_helper(matrix, n, G):

        nonlocal new_node

        if n == 2:
            print("d add_edge (%s,%s):%s" % (0, 1, matrix[0, 1]))
            G.add_edge(0, 1, weight=matrix[0, 1])
            return

        limblen = limblength(n - 1, matrix)
        i, k = find_i_k(matrix, n - 1, limblen)
        x = matrix[i, n - 1] - limblen

        print("n=%s limblen=%s i=%s k=%s x=%s" % (n, limblen, i, k, x))

        additive_recur_helper(matrix[0 : n - 1, 0 : n - 1], n - 1, G)

        v = node_at_distance(G, i, k, x, matrix[i, k], new_node)
        if v == new_node:
            new_node += 1

        print("node_at_distance %s from %s is %s" % (x, i, v))

        print("e add_edge (%s,%s):%s" % (v, n - 1, limblen))
        G.add_edge(v, n - 1, weight=limblen)

        # draw graph if small
        if len(G) < 30:
            global plot_cnt
            pos = nx.kamada_kawai_layout(G)
            labels = nx.get_edge_attributes(G, "weight")
            nx.draw(G, pos, with_labels=True)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            plt.draw()
            plt.savefig("Graph" + str(plot_cnt) + ".png", format="PNG")
            plt.clf()
            plot_cnt += 1

        return

    additive_recur_helper(matrix, n, G)

    return


if __name__ == "__main__":

    with open("dataset_10330_6 (3).txt") as f:
        data = f.read().splitlines()

    n = int(data[0])

    matrix = []
    for line in data[1:]:
        matrix.append([int(i) for i in line.split()])

    matrix = np.array(matrix)

    G = nx.Graph()
    n = len(matrix)
    additive_phylogeny(matrix, n, G)

    wt = G.edges.data("weight")
    lent = G.edges.data("len")
    print(lent)

    out = []
    for w in wt:
        out.append("%s->%s:%s" % (w[0], w[1], w[2]))
        out.append("%s->%s:%s" % (w[1], w[0], w[2]))

    out.sort()
    with open("out.txt", "w") as f:
        for o in out:
            f.write(o + "\n")

    # draw graph if small
    if len(G) < 100:
        plt.figure(figsize=(60, 40))
        # pos = nx.planar_layout(G)
        pos = nx.kamada_kawai_layout(G)
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx(G, pos)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.draw()  # pyplot draw()
        plt.savefig("Graph_out.png", format="PNG")
        plt.clf()
