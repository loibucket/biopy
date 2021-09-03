import networkx as nx
import matplotlib.pyplot as plt
import os
import pathlib
import copy
import pygraphviz

from datetime import datetime


def two_nearest_neighbors(G, e1, e2):
    """
    make graphs of 2 of the nearest neighbors of graph G at edge e1-e2
    """

    e1n = G.neighbors(e1)
    e2n = G.neighbors(e2)

    list1 = [e for e in list(e1n) if e not in [e1, e2]]
    list2 = [e for e in list(e2n) if e not in [e1, e2]]

    print(e1, list1, e2, list2)

    assert len(list1) > 1 and len(list2) > 1

    glist = []

    for i in range(2):

        GG = copy.deepcopy(G)

        GG.remove_edge(list1[0], e1)
        GG.add_edge(list1[0], e2)

        GG.remove_edge(list2[i], e2)
        GG.add_edge(list2[i], e1)

        glist.append(GG)

    return glist


if __name__ == "__main__":
    # open text file
    with open("dataset_10336_6 (2).txt") as f:
        data = f.read().splitlines()
        e1, e2 = data[0].split()
        d = data[1:]

    # build graph
    G = nx.Graph()
    for line in d:
        a, b = line.split("->")
        G.add_edge(a, b)

    glist = two_nearest_neighbors(G, e1, e2)

    with open("dataset_10336_6out", "w") as f:
        for i, G in enumerate(glist):

            for edge in G.edges:
                f.write(edge[0] + "->" + edge[1] + "\n")
                f.write(edge[1] + "->" + edge[0] + "\n")
            if i == 0:
                f.write("\n")

            # draw graph file, need to make a log folder
            if True:
                ## draw graph boilerplate ##
                pos = nx.nx_agraph.graphviz_layout(G, prog="neato")
                nx.draw(G, pos, with_labels=True)

                p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
                plt.savefig(p)
                plt.clf()
                ## end graph ##
