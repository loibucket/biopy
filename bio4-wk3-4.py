import logging

import re
import networkx as nx
import matplotlib.pyplot as plt
import os
import pathlib
import copy
import pygraphviz
import math

from datetime import datetime


def add_root(G, maxnode):
    """
    break the edge between the max node and next largest node connected to max node
    insert a rootnode between the nodes
    """
    rootnode = maxnode + 1
    a = maxnode
    b = maxnode - 1
    while not G.has_edge(a, b):
        b -= 1
    G.remove_edge(a, b)
    G.add_edge(rootnode, a)
    G.add_edge(rootnode, b)

    nx.set_node_attributes(G, {rootnode: 0}, name="leaf")
    nx.set_node_attributes(G, {rootnode: ""}, name="char")
    nx.set_node_attributes(G, {rootnode: 0}, name="tag")


def parsimony(G, leafnodes, maxnode):
    """
    compute the min parsimony score for graph
    """
    g_ref = copy.deepcopy(G)
    graph_list = []
    seq_sample = G.nodes[0]["char"]
    score_sum = 0
    # make a separate tree for each nucleotide position
    for pos in range(len(seq_sample)):
        GG = copy.deepcopy(G)
        # update leaf node values
        for node in leafnodes:
            newchar = GG.nodes[node]["char"][pos]
            nx.set_node_attributes(GG, {node: 1}, name="leaf")
            nx.set_node_attributes(GG, {node: newchar}, name="char")
            nx.set_node_attributes(GG, {node: 1}, name="tag")
            dct = {}
            for sym in ["A", "C", "G", "T"]:
                dct[sym] = 1 if newchar != sym else 0
            nx.set_node_attributes(GG, {node: dct}, name="score")
        # run small parsimony on the tree
        small_parsimony(GG)
        # get the root symbol and score
        root_char, root_score = min(GG.nodes[maxnode]["score"].items(), key=lambda x: x[1])
        GG.nodes[maxnode]["char"] = root_char
        # fill all internal node symbols
        char_filler(GG, len(leafnodes), maxnode)
        # store graph and the score
        graph_list.append(GG)
        score_sum += root_score

    # make a single tree with entire sequence at each node
    combine_g = combine_graphs(graph_list, maxnode)

    return score_sum, combine_g


def combine_graphs(graph_list, maxnode):
    """
    combine trees of single nucleotide nodes into a tree of sequence nodes
    """
    GG = graph_list[0]
    # combine chars in each tree to make a tree with sequences
    for tree in graph_list[1:]:
        for node in range(maxnode + 1):
            GG.nodes[node]["char"] += tree.nodes[node]["char"]
    return GG


def small_parsimony(G):
    """
    complete the a partial small parsimony graph with only leaf sequences
    """
    ripes = ripe_nodes(G)
    while ripes:
        v = ripes[0]
        G.nodes[v]["tag"] = 1
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
            succ = list(G.successors(n))
            if sum([G.nodes[s]["tag"] for s in succ]) == len(succ):
                ripes.append(n)
    return ripes


def char_filler(G, n, start_node):
    """
    adds a char to intermediate nodes
    for each node, if char=parent_sym has lowest score, use parent_sym for the node's char
    else use the char with the best score
    """
    explore = list(G.successors(start_node))
    while explore:
        new_explore = []
        for node in explore:
            parent = list(G.predecessors(node))[0]
            parent_sym = G.nodes[parent]["char"]

            scores = G.nodes[node]["score"]
            min_sco = min(scores.values())

            if scores[parent_sym] == min_sco:
                G.nodes[node]["char"] = parent_sym
            else:
                best_char, best_score = min(G.nodes[node]["score"].items(), key=lambda x: x[1])
                G.nodes[node]["char"] = best_char
            new_explore += G.successors(node)
        explore = new_explore


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


def draw_graph(G):
    """
    draw graph G to file
    """
    ## draw graph boilerplate ##
    # pos = nx.kamada_kawai_layout(G)
    pos = nx.nx_agraph.graphviz_layout(G, prog="dot")
    nx.draw(G, pos, with_labels=True)

    pos_off = copy.deepcopy(pos)
    for k in pos_off.keys():
        pos_off[k] = (pos_off[k][0], pos_off[k][1] - 10)

    # labels = nx.get_node_attributes(G, "char")

    labels = nx.get_node_attributes(G, "score")
    for key, val in labels.items():
        labels[key] = str(list(val.values())) + "\n" + str(G.nodes[key]["char"])

    node_labels = labels
    nx.draw_networkx_labels(G, pos_off, labels=node_labels)

    edge_labels = nx.get_edge_attributes(G, "dist")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    p = os.path.join(pathlib.Path(__file__).parent.resolve(), "logs", "graph%s.png" % (datetime.now().strftime("%Y-%m-%dT%H%M%S.%f")[:-3]))
    plt.savefig(p)
    plt.clf()
    ## end graph ##


def g_nearest_neighbors(G, e1, e2):
    """
    make graphs of the nearest neighbors of graph G at edge e1-e2
    """
    print("edge", e1, e2)
    e1n = G.neighbors(e1)
    e2n = G.neighbors(e2)
    list1 = [e for e in list(e1n) if e not in [e1, e2]]
    list2 = [e for e in list(e2n) if e not in [e1, e2]]
    glist = []
    per = 0
    for i, _ in enumerate(list1):
        for j, _ in enumerate(list2):
            per += 1
            GG = copy.deepcopy(G)
            GG.remove_edge(e1, list1[i])
            GG.add_edge(e2, list1[i])
            GG.remove_edge(e2, list2[j])
            GG.add_edge(e1, list2[j])
            glist.append(GG)
    return glist


def get_internal_edges(G, leafnodes):
    """
    get all internal edges
    """
    all_edges = G.edges
    internals = []
    for edge in all_edges:
        if len(leafnodes) == sum([i not in edge for i in leafnodes]):
            internals.append(edge)
    return internals


if __name__ == "__main__":

    # open text file
    with open("dataset_10336_8 (5).txt") as f:
        data = f.read().splitlines()
        n = int(data[0])
        d = data[1:]

    # clean up data
    d = sorted(d)
    d = d[:-n]
    internals = []
    leafs = []
    for line in d:
        has_letters = re.search("[a-zA-Z]", line)
        if has_letters:
            leafs.append(line)
            continue
        a, b = [int(c) for c in line.split("->")]
        if a > b:
            internals.append(line)

    leafs.sort()
    internals.sort()

    # write out a sample sequence in the file
    seq_sample = leafs[1].split("->")[1]
    print("seq_sample", seq_sample)

    # make graphs
    graph_list = []
    score_sum = 0
    maxnode = int(internals[-1].split("->")[0])  # highest number node

    # build the starting graph
    G = nx.DiGraph()
    # for leaf nodes, add to graph node number, edge to parent, char
    leafnodes = []
    for node, line in enumerate(leafs):
        node = int(node)
        leafnodes.append(node)
        parent, sequence = line.split("->")
        parent = int(parent)
        G.add_node(node)
        char = sequence
        nx.set_node_attributes(G, {node: 1}, name="leaf")
        nx.set_node_attributes(G, {node: char}, name="char")
        nx.set_node_attributes(G, {node: 1}, name="tag")
        dct = {}
        for sym in ["A", "C", "G", "T"]:
            dct[sym] = 1 if char != sym else 0
        nx.set_node_attributes(G, {node: dct}, name="score")
        G.add_edge(parent, node)
    # for non-leaf, add nodes and edges to graph, add blank char
    for line in internals:
        a, b = line.split("->")
        a, b = int(a), int(b)
        G.add_edge(a, b)
        nx.set_node_attributes(G, {a: 0, b: 0}, name="leaf")
        nx.set_node_attributes(G, {a: "", b: ""}, name="char")
        nx.set_node_attributes(G, {a: 0, b: 0}, name="tag")

    # loop through graphs
    best_score = 2 ** 32
    this_score = 2 ** 32 - 1
    edges_collection = []

    epoch = 0
    while best_score > this_score:
        epoch += 1
        print("epoch", epoch)
        best_score = this_score

        # create all nearest neighor interchange
        graph_neighbors = [G]
        for edge in get_internal_edges(G, leafnodes):
            e1, e2 = edge
            graph_neighbors += g_nearest_neighbors(G, e1, e2)

        # modify graphs to add root node
        for G in graph_neighbors:
            add_root(G, maxnode)
        maxnode += 1  # maxnode is root node

        ith_g = -1
        min_gscore = math.inf
        G_save = None
        # run through each graph and save best score
        for i, G in enumerate(graph_neighbors):
            g_score, combine_g = parsimony(G, leafnodes, maxnode)
            if g_score < min_gscore:
                ith_g = i
                G_save = combine_g
                min_gscore = g_score

            print("ith graph", i, "g_score", g_score)

        print("best graph", ith_g, "min_gscore", min_gscore)

        # remove extra node
        a, b = G_save.successors(maxnode)
        G_save.remove_edge(maxnode, a)
        G_save.remove_edge(maxnode, b)
        G_save.add_edge(max(a, b), min(a, b))
        G_save.remove_node(maxnode)
        maxnode -= 1

        # add to results
        draw_graph(G_save)
        edges_collection.append([str(min_gscore)] + edge_maker(G_save))

        # reset graph info
        for node in G_save.nodes:
            if not G_save.nodes[node]["leaf"]:
                G_save.nodes[node]["tag"] = 0
                G_save.nodes[node]["char"] = 0
                G_save.nodes[node]["score"] = {}

        G = G_save
        this_score = min_gscore

    ## write out result file
    with open("dataset_10336_8out.txt", "w") as f:
        for string_edges in edges_collection[:-1]:
            for line in string_edges:
                f.write(line + "\n")
            f.write("\n")
