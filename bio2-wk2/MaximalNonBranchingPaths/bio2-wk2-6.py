from collections import defaultdict


def def_list():
    return []


def maximal_non_branching_paths(adj_list):
    """
    split adjacency list into a set of non-branching paths
    """

    outbound = defaultdict(def_list)
    inbound = defaultdict(def_list)
    node_set = set()
    # build outbound map
    # build inbound map
    for adj in adj_list:
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

    def one_in_one_out(node):
        if len(inbound[node]) == 1 and len(outbound[node]) == 1:
            return True
        return False

    paths = []
    used_set = set()
    for node in node_set:
        if not one_in_one_out(node):
            if len(outbound[node]) > 0:
                used_set.add(node)
                for w in outbound[node]:
                    used_set.add(w)
                    non_branching_path = [node, w]
                    while one_in_one_out(w):
                        u = outbound[w][0]
                        used_set.add(u)
                        non_branching_path.append(u)
                        w = u
                    paths.append(non_branching_path)

    leftover = node_set.difference(used_set)
    cir_paths = []
    while leftover:
        x = outbound[next(iter(leftover))][0]
        leftover.remove(x)
        y = outbound[x][0]
        cycle = [x, y]
        while cycle[0] != cycle[-1]:
            leftover.remove(y)
            y = outbound[cycle[-1]][0]
            cycle.append(y)
        cir_paths.append(cycle)

    return paths + cir_paths


import os

if __name__ == "__main__":

    files = [f for f in os.listdir('./inputs')]

    for i, f in enumerate(files):
        print(i, f)

        with open("inputs/" + f) as dataset:

            adj_list = dataset.read().splitlines()
            a = maximal_non_branching_paths(adj_list)
            out = []
            for line in a:
                out.append("->".join(line))
            out.sort()

            ## output
            with open(f"out_{i}.txt", "w") as file:
                for j, line in enumerate(a):
                    file.write(out[j] + "\n")

            try:
                ## expected output
                with open("outputs/" + f) as results:
                    res = results.read().splitlines()
                    res.sort()

                ## compare with expected output
                with open(f"out_e{i}.txt", "w") as file:
                    for j, line in enumerate(a):
                        file.write(out[j] + " ----- " + res[j] + "\n")
            except Exception:
                pass
