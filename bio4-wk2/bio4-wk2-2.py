import logging

from datetime import datetime
import numpy as np
import networkx as nx
import math
import pandas as pd
import matplotlib.pyplot as plt
import os
import pathlib
import copy


def upgma(D, n):
    """
    Create an Ultrametric Evolutionary Tree of n species from a distance matrix-like D, given as a nested dictionary
    """
    G = nx.Graph()

    for i in range(n):
        G.add_node(i)
        nx.set_node_attributes(G, {i: 0}, name="age")
        nx.set_node_attributes(G, {i: 1}, name="size")

    while len(D) > 1:

        new_node = max(G.nodes) + 1

        min_dex, min_val = find_min(D)
        a, b = min_dex[0], min_dex[1]
        size = G.nodes[a]["size"] + G.nodes[b]["size"]

        D[new_node] = {}
        for k in D.keys():
            if new_node == k:
                D[new_node][k] = 0
                continue
            D[new_node][k] = (D[a][k] * G.nodes[a]["size"] + D[b][k] * G.nodes[b]["size"]) / size
            D[k][new_node] = D[new_node][k]

        rem_rowcol(D, a)
        rem_rowcol(D, b)
        print_dct(D)

        age = min_val / 2.0
        G.add_node(new_node)
        nx.set_node_attributes(G, {new_node: age}, name="age")
        nx.set_node_attributes(G, {new_node: size}, name="size")
        G.add_edge(a, new_node, length=age - G.nodes[a]["age"])
        G.add_edge(b, new_node, length=age - G.nodes[b]["age"])

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
    find index of minval in nested dct
    """
    res_dict = {}

    for k, v in nested_dct.items():
        for k2, v2 in v.items():
            if v2 > 0:
                res_dict[(k, k2)] = v2

    minval = min(res_dict.values())
    res = [k for k, v in res_dict.items() if v == minval]

    return res[0], minval


def print_dct(nested_dct):
    """
    print a nested dct into a matrix like
    """

    df = pd.DataFrame.from_dict(nested_dct, orient="index")
    print(df)


if __name__ == "__main__":

    with open("dataset_10332_8tt.txt") as f:
        data = f.read().splitlines()

        n = int(data[0])
        d = data[1:]

    dct = {}

    for i, line in enumerate(d):
        dct[i] = {}
        for j, val in enumerate([int(i) for i in line.split()]):
            dct[i][j] = val

    print_dct(dct)

    G = upgma(dct, n)

    for a, b, data in G.edges(data=True):
        print(str(a) + "->" + str(b) + ":" + "%.3f" % (data["length"]))
        print(str(b) + "->" + str(a) + ":" + "%.3f" % (data["length"]))

    ## draw graph ##
    pos = nx.kamada_kawai_layout(G)
    pos_off = copy.deepcopy(pos)
    for k in pos_off.keys():
        pos_off[k] = pos_off[k] + 0.08

    nx.draw(G, pos, with_labels=True)

    node_labels = nx.get_node_attributes(G, "age")
    nx.draw_networkx_labels(G, pos_off, labels=node_labels)

    edge_labels = nx.get_edge_attributes(G, "length")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    plt.savefig(p)
    plt.clf()
    ## end draw ##

    ## create logger ##
    logger = logging.getLogger(__name__)

    logdir = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs")
    if not os.path.exists(logdir):
        os.makedirs(logdir)

    f = os.path.join(logdir, "log_%s.log" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    f_handler = logging.FileHandler(f)
    f_format = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s: %(message)s")
    f_handler.setFormatter(f_format)
    logger.addHandler(f_handler)

    logging.getLogger().setLevel(logging.DEBUG)
    logger.debug("test debug message")
    logger.info("test info message")
    logger.warning("test warning message")
    logger.error("test error message")
    ## end create ##
