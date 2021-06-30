import biopy as bp
from collections import defaultdict
import os

def def_list():
    return []


with open("wk2quiz1.txt") as dataset:
    kmers = dataset.read().splitlines()
    kmers = [k for k in kmers if k !=""]
    print("kmers",kmers)
    out = bp.patterns_to_sequence(kmers, debug=False)
    print("seq", out, "\n")

with open("wk2quiz2.txt") as dataset:
    adj_list = dataset.read().splitlines()
    adj_list = [k for k in adj_list if k !=""]
    # build outbound map
    # build inbound map
    outbound = defaultdict(def_list)
    inbound = defaultdict(def_list)
    node_set = set()
    for adj in adj_list:
        adj = adj.replace(" ", "")
        l, r = adj.split("->")
        node_set.add(l)
        if "," in r:
            ars_list = r.split(",")
            outbound[l] += ars_list
            for node in ars_list:
                node_set.add(node)
                inbound[node].append(l)
        else:
            node_set.add(r)
            outbound[l].append(r)
            inbound[r].append(l)

    for n in sorted(node_set):
        print("node:", n, ":", len(inbound[n]),"in", inbound[n],  len(outbound[n]),"out", outbound[n])
    print("")

with open("wk2quiz3.txt") as dataset:
    pairs = dataset.read().splitlines()
    pairs = [k for k in pairs if k !=""]
    pairs = [p[1:-1] for p in pairs]
    seq = bp.pairs_to_sequence(3, 1, pairs, debug=False)
    print(seq)

# read breaking CAN transform reads with imperfect coverage into reads with perfect coverage.

# every Eulerian path in the de Bruijn graph constructed from a k-mer composition DOES NOT HAVE TO spell out a solution to the String Reconstruction Problem.
