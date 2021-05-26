from collections import defaultdict
import json
import copy
from collections import deque


def def_list():
    return []


def def_val():
    return 0


def euler_cycle(adjacency_list):
    """
    build an euler path from an adjacency list
    """
    unique_mers = set()
    # build dict from list
    mers_map = defaultdict(def_list)
    mers_count = defaultdict(def_val)
    seq_length = 1
    for l in adjacency_list:
        a, b = l.split("->")
        a = a.strip()
        unique_mers.add(a)
        mers = [n.strip() for n in b.split(",")]
        mers_map[a] = mers
        seq_length += len(mers)
        for m in mers:
            mers_count[m] += 1

    # start with first vertex, try to build on it
    stack = []
    location = adjacency_list[0].split("->")[0].strip()
    # ex. location = 6

    # build inbound dict
    mers_inbound = defaultdict(def_list)
    for k, v in mers_map.items():
        for mer in v:
            mers_inbound[mer].append(k)
            unique_mers.add(mer)

    # find starting location
    for mer in unique_mers:
        if len(mers_map[mer]) > len(mers_inbound[mer]):
            location = mer
            break

    circuit = []

    while True:
        # http://www.graph-magics.com/articles/euler.php
        if location in mers_map and len(mers_map[location]) > 0:
            stack.append(location)
            location = mers_map[location].pop()
        else:
            circuit.append(location)
            location = stack.pop() if stack else None

        if len(circuit) >= seq_length:
            break

    circuit.reverse()
    return circuit


if __name__ == "__main__":

    datasets = ["dataset_203_sample.txt", "dataset_203_2-3.txt", "dataset_203_6-2.txt"]
    for i, d in enumerate(datasets):
        with open(d, "r") as f:
            adjanceny_list = f.read().splitlines()
            seq = euler_cycle(adjanceny_list)
            file = open('out_'+str(i)+'.txt', 'w')
            file.write("->".join(str(n) for n in seq))
            file.close()
