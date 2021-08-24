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


def small_parsimony(G):
    """
    complete the a partial small parsimony graph with only leaf sequences
    """
    ripes = ripe_nodes(G)
    while ripes:
        v = ripes[0]
        G.nodes[v]["tag"] = 1
        dau, son = G.successors(v)
        nx.set_node_attributes(G, {v: score_builder(G, v)}, name="score")
        ripes = ripe_nodes(G)


def score_builder(G, v):
    """
    build score map for internal nodes
    """
    v_score = {}
    for v_sym in ["A", "C", "G", "T"]:
        v_sco = 0
        for child in G.successors(v):
            min_sco = math.inf
            for child_sym in ["A", "C", "G", "T"]:
                alpha = 1 if v_sym != child_sym else 0
                sco = G.nodes[child]["score"][child_sym] + alpha
                min_sco = min(min_sco, sco)
            v_sco += min_sco
        v_score[v_sym] = v_sco
    return v_score


def ripe_nodes(G):
    """
    get all the ripe nodes (childs ar both tag=1)
    """
    ripes = []
    for n in G.nodes:
        if not G.nodes[n]["leaf"] and G.nodes[n]["tag"] == 0:
            a, b = G.successors(n)
            if G.nodes[a]["tag"] == 1 and G.nodes[b]["tag"] == 1:
                ripes.append(n)
    return ripes


def char_filler(G, n, maxnode):
    """
    adds a char to intermediate nodes
    for each node, if char=parent_sym has lowest score, use parent_sym for the node's char
    else use the char with the best score
    """
    for node in reversed(range(n, maxnode)):
        parent = list(G.predecessors(node))[0]
        parent_sym = G.nodes[parent]["char"]

        scores = G.nodes[node]["score"]
        min_sco = min(scores.values())

        if scores[parent_sym] == min_sco:
            G.nodes[node]["char"] = parent_sym
        else:
            best_char, best_score = min(G.nodes[node]["score"].items(), key=lambda x: x[1])
            G.nodes[node]["char"] = best_char


def edge_maker(G):
    """
    creates the edges in the format for submit, with each line as an item in the list
    """
    string_edges = []

    for edge in G.edges:
        a, b = edge[0], edge[1]
        dist = str(ham_dist(G.nodes[a]["char"], G.nodes[b]["char"]))
        string_edges.append(G.nodes[a]["char"] + "->" + G.nodes[b]["char"] + ":" + dist)
        string_edges.append(G.nodes[b]["char"] + "->" + G.nodes[a]["char"] + ":" + dist)

    return sorted(string_edges)


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


if __name__ == "__main__":

    # open text file
    with open("dataset_10335_10 (2).txt") as f:
        data = f.read().splitlines()
        n = int(data[0])
        d = data[1:]

    # write out a sample sequence in the file
    seq_sample = d[1].split("->")[1]
    print("seq_sample", seq_sample)

    graph_list = []
    score_sum = 0
    maxnode = int(d[-1].split("->")[0])  # highest number node

    # make a separate graph for each pos in sequence
    for pos in range(len(seq_sample)):
        G = nx.DiGraph()
        # for leaf nodes, add to graph node number, edge to parent, char
        for node, line in enumerate(d[:n]):
            node = int(node)
            parent, sequence = line.split("->")
            parent = int(parent)
            G.add_node(node)
            char = sequence[pos]
            nx.set_node_attributes(G, {node: 1}, name="leaf")
            nx.set_node_attributes(G, {node: char}, name="char")
            nx.set_node_attributes(G, {node: 1}, name="tag")
            dct = {}
            for sym in ["A", "C", "G", "T"]:
                dct[sym] = 1 if char != sym else 0
            nx.set_node_attributes(G, {node: dct}, name="score")
            G.add_edge(parent, node)
        # for non-leaf, add nodes and edges to graph, add blank char
        for line in d[n:]:
            a, b = line.split("->")
            a, b = int(a), int(b)
            G.add_edge(a, b)
            nx.set_node_attributes(G, {a: 0, b: 0}, name="leaf")
            nx.set_node_attributes(G, {a: "", b: ""}, name="char")
            nx.set_node_attributes(G, {a: 0, b: 0}, name="tag")

        # run small parsimony to update graph G
        small_parsimony(G)
        # pull results from graph
        best_char, best_score = min(G.nodes[maxnode]["score"].items(), key=lambda x: x[1])
        G.nodes[maxnode]["char"] = best_char
        score_sum += best_score

        print("root", best_score, best_char)

        # fill the graph with char for each node, save to graph list
        char_filler(G, n, maxnode)
        graph_list.append(G)

    print("score", score_sum)

    G = graph_list[0]

    # combine chars in each tree to make a tree with sequences
    for tree in graph_list[1:]:
        for node in range(maxnode + 1):
            G.nodes[node]["char"] += tree.nodes[node]["char"]

    string_edges = edge_maker(G)

    # write out result file
    with open("dataset_10335_10out.txt", "w") as f:
        f.write(str(score_sum) + "\n")
        for line in string_edges:
            f.write(line + "\n")

    # draw graph file
    if True:
        ## draw graph boilerplate ##
        # pos = nx.kamada_kawai_layout(G)
        pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
        nx.draw(G, pos, with_labels=True)

        pos_off = copy.deepcopy(pos)
        for k in pos_off.keys():
            pos_off[k] = (pos_off[k][0], pos_off[k][1] - 10)

        labels = nx.get_node_attributes(G, "char")
        # for key, val in labels.items():
        #     labels[key] = str(list(val.values())) + " " + str(G.nodes[key]["char"])

        node_labels = labels
        nx.draw_networkx_labels(G, pos_off, labels=node_labels)

        edge_labels = nx.get_edge_attributes(G, "dist")
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

        p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S")))
        plt.savefig(p)
        plt.clf()
        ## end graph ##

    if False:
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
