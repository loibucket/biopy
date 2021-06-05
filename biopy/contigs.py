from collections import defaultdict
import biopy as bp
import os


def def_list():
    return []


def contigs(adj_list):
    """
    convert adjacency list into a set of non-branching contigs, or "maximal non-branching path"
    """
    # build outbound map
    # build inbound map
    outbound = defaultdict(def_list)
    inbound = defaultdict(def_list)
    node_set = set()
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

    # is node 1 in and 1 out
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

    out = []
    for p in (paths + cir_paths):
        out.append("->".join(p))

    return out


if __name__ == "__main__":

    files = [f for f in os.listdir('./temp')]

    for i, f in enumerate(files):
        print(i, f)

        with open("temp/Contigs/inputs" + f) as dataset:
            kmers = dataset.read().splitlines()
            adj_list = bp.debrujin_graph(kmers)
            contigs = bp.contigs(adj_list)

            print(contigs())
