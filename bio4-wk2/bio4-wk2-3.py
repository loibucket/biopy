## logging wrapper
import logging

from datetime import datetime
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib


def neighbor_joining(D, n):
    """
    Create a neighbor joining tree of n species from a distance matrix-like D, given as a nested dictionary
    return the networkx graph
    """

    # start with a graph of disconnected species nodes
    G = nx.Graph()
    for i in range(n):
        G.add_node(i)

    # build graph edges and reduce D matrix-like until it is 2x2
    while len(D) > 2:
        D_pri, total_dist = d_prime(D)
        d_reduce(D, D_pri, total_dist, G)

    print_dct(D)

    # join the last 2 nodes in D
    a, b = D.keys()
    G.add_edge(a, b, length=D[a][b])

    return G


def rem_rowcol(nested_dct, ith_rowcol):
    """
    remove the ith row and col from the matrix-like nested dct
    """
    for k in nested_dct.keys():
        nested_dct[k].pop(ith_rowcol)
    nested_dct.pop(ith_rowcol)


def find_min(nested_dct):
    """
    find first minval and its index in nested dct
    """
    res_dict = {}

    for k, v in nested_dct.items():
        for k2, v2 in v.items():
            if v2 != 0:
                res_dict[(k, k2)] = v2

    minval = min(res_dict.values())
    res = [k for k, v in res_dict.items() if v == minval]

    return res[0], minval


def print_dct(nested_dct):
    """
    print a nested dct into a matrix-like
    """
    df = pd.DataFrame.from_dict(nested_dct, orient="index")
    print(df)


def d_prime(D):
    """
    create neighbor joining matrix-like D_prime from distance matrix-like D
    """
    total_dist = {}
    for k, v in D.items():
        total_dist[k] = sum(v.values())

    D_pri = {}
    n = len(D)

    for i in D.keys():
        D_pri[i] = {}
        for j in D[i].keys():
            if i == j:
                D_pri[i][j] = 0
                continue
            D_pri[i][j] = (n - 2) * D[i][j] - total_dist[i] - total_dist[j]

    return D_pri, total_dist


def d_reduce(D, D_pri, total_dist, G):
    """
    reduce D by one row one col by joining 2 closest neighbors per D_pri
    add the joining to the graph G
    """
    print_dct(D)
    print_dct(D_pri)

    n = len(D)
    new_node = max(D.keys()) + 1
    min_dex, min_val = find_min(D_pri)

    i = min_dex[0]
    j = min_dex[1]

    D[new_node] = {}
    for k in D.keys():
        if k == new_node:
            D[k][k] = 0
            continue
        D[new_node][k] = 0.5 * (D[k][i] + D[k][j] - D[i][j])
        D[k][new_node] = D[new_node][k]

    delta_ij = (total_dist[i] - total_dist[j]) / (n - 2)
    limblen_i = 0.5 * (D[i][j] + delta_ij)
    limblen_j = 0.5 * (D[i][j] - delta_ij)

    G.add_node(new_node)
    G.add_edge(i, new_node, length=limblen_i)
    G.add_edge(j, new_node, length=limblen_j)

    rem_rowcol(D, i)
    rem_rowcol(D, j)


if __name__ == "__main__":

    with open("dataset_10333_7tt.txt") as f:
        data = f.read().splitlines()
        n = int(data[0])
        d = data[1:]

    dct = {}

    for i, line in enumerate(d):
        dct[i] = {}
        for j, val in enumerate([int(i) for i in line.split()]):
            dct[i][j] = val

    G = neighbor_joining(dct, n)

    for a, b, data in G.edges(data=True):
        print(str(a) + "->" + str(b) + ":" + "%.3f" % (data["length"]))
        print(str(b) + "->" + str(a) + ":" + "%.3f" % (data["length"]))

    ## draw graph ##
    pos = nx.kamada_kawai_layout(G)
    nx.draw(G, pos, with_labels=True)
    edge_labels = nx.get_edge_attributes(G, "length")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    pt = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    plt.savefig(pt)
    plt.clf()
    ## end draw ##

    ## create logger ##
    # logger = logging.getLogger(__name__)

    # logdir = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs")
    # if not os.path.exists(logdir):
    #     os.makedirs(logdir)

    # f = os.path.join(logdir, "log_%s.log" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    # f_handler = logging.FileHandler(f)
    # f_format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s: %(message)s")
    # f_handler.setFormatter(f_format)
    # logger.addHandler(f_handler)

    # logging.getLogger().setLevel(logging.DEBUG)
    # logger.debug("test debug message")
    # logger.info("test info message")
    # logger.warning("test warning message")
    # logger.error("test error message")
    ## end create ##
