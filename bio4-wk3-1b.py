import logging

import numpy as np
import networkx as nx
import math
import matplotlib.pyplot as plt
import os
import pathlib
import copy
import math
import pygraphviz

from datetime import datetime


def ham_dist(p, q):
    """
    hamming distance is the number of mismatches between equal length sequences p and q
    returns integer
    """
    count = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            count += 1
    return count


def dee(pattern, seq):
    """
    find the min possible ham distance between a pattern and seq at all possible binding locations
    """
    k = len(pattern)
    d = math.inf
    for i in range(len(seq) - k + 1):
        ham = ham_dist(pattern, seq[i : i + k])
        if ham < d:
            d = ham
    return d


def sumDee(pattern, dna):
    """
    sum the score for dna
    """
    sumD = 0
    for seq in dna:
        sumD += dee(pattern, seq)
    return sumD


def neighbors(pattern, d):
    """
    'mismatch-permutations'
    given a pattern, neighbors are all the possible permutation of patterns that have d or fewer mismatches
    recursive function
    returns a string of space-separated patterns
    """
    tides = set(["A", "C", "G", "T"])
    if d == 0:
        return set([pattern])
    if len(pattern) == 1:
        return tides
    neighborhood = set([])
    suffix_neighbors = neighbors(pattern[1:], d)
    for text in suffix_neighbors:
        if ham_dist(pattern[1:], text) < d:
            for tide in tides:
                neighborhood.add(tide + text)
        else:
            neighborhood.add(pattern[0] + text)
    return neighborhood


def medianString(dna, k):
    """
    the kmer with the lowest sum d across the dna
    """
    score = math.inf
    median = ""
    medlist = []
    kmers = neighbors("A" * k, k)
    for pattern in kmers:
        if sumDee(pattern, dna) < score:
            score = sumDee(pattern, dna)
            median = pattern

    # return only 1 median string
    return median

    # return all median strings
    # for pattern in kmers:
    #     if sumDee(pattern, dna) == score:
    #         return pattern
    #         medlist.append(pattern)

    # return medlist


def small_parsimony(G, n, maxnode):
    """
    complete the a partial small parsimony graph with only leaf sequences
    """
    # run on non leaf nodes
    for node in range(n, maxnode + 1):
        # get sequences of child nodes
        a, b = G.predecessors(node)
        sequence = nx.get_node_attributes(G, "seq")
        dna = [sequence[a], sequence[b]]
        # get median string
        med_string = medianString(dna, len(sequence[0]))
        nx.set_node_attributes(G, {node: med_string}, name="seq")
        # set distance based on median string
        G[a][node]["dist"] = ham_dist(sequence[a], med_string)
        G[b][node]["dist"] = ham_dist(sequence[b], med_string)


if __name__ == "__main__":

    with open("dataset_10335_10s.txt") as f:
        data = f.read().splitlines()

        n = int(data[0])
        d = data[1:]

    G = nx.DiGraph()

    pos = 0

    # for leaf nodes, add to graph node number, edge to parent, sequence
    for node, line in enumerate(d[:n]):
        node = int(node)
        parent, sequence = line.split("->")
        parent = int(parent)
        G.add_node(node)
        nx.set_node_attributes(G, {node: sequence[pos]}, name="seq")
        G.add_edge(node, parent)

    # for non-leaf, add nodes and edges to graph, add blank sequence
    for line in d[n:]:
        a, b = line.split("->")
        a, b = int(a), int(b)
        G.add_edge(b, a)
        nx.set_node_attributes(G, {a: ""}, name="seq")
        nx.set_node_attributes(G, {b: ""}, name="seq")

    # maxnode = a

    # small_parsimony(G, n, maxnode)

    ## draw graph boilerplate ##
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    for k in pos.keys():
        pos[k] = (pos[k][0], -pos[k][1])
    nx.draw(G, pos, with_labels=True)

    pos_off = copy.deepcopy(pos)
    for k in pos_off.keys():
        pos_off[k] = (pos_off[k][0], pos_off[k][1] - 10)
    node_labels = nx.get_node_attributes(G, "seq")
    nx.draw_networkx_labels(G, pos_off, labels=node_labels)

    edge_labels = nx.get_edge_attributes(G, "dist")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
    plt.savefig(p)
    plt.clf()
    ## end graph ##

    ## logger boilerplate ##
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
    ## end logger ##
