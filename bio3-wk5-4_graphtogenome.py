from collections import deque
import copy


def cycle_to_chromosome(nodes):
    """
    convert a chromosome in nodes format to synteny blocks format
    """
    chromo = [0] * (int(len(nodes) / 2) + 1)

    nod = [0] + nodes.copy()

    for j in range(1, int(len(nodes) / 2) + 1):
        if nod[2 * j - 1] < nod[2 * j]:
            chromo[j] = int(nod[2 * j] / 2)
        else:
            chromo[j] = -int(nod[2 * j - 1] / 2)

    return chromo[1:]


def graph_to_genome(edges_graph):
    """
    convert a list of colored edges to a genome in synteny blocks format
    """
    colored_edges = copy.deepcopy(edges_graph)

    d_head = dict()
    d_tail = dict()

    for edge in colored_edges:
        d_head[edge[0]] = edge[1]
        d_tail[edge[1]] = edge[0]

    genome = []
    nodes = []

    # print(colored_edges)

    while d_head:

        # print("nodes", nodes)

        if nodes == []:
            key = next(iter(d_head))
            nodes = [key, d_head[key]]
            d_tail.pop(d_head[key])
            d_head.pop(key)
            continue

        if nodes[0] % 2 == 0:
            a = nodes[0] - 1
        else:
            a = nodes[0] + 1

        if nodes[-1] % 2 == 0:
            b = nodes[-1] - 1
        else:
            b = nodes[-1] + 1

        added = False

        if a in d_head.keys():
            nodes = [d_head[a], a] + nodes
            d_tail.pop(d_head[a])
            d_head.pop(a)
            added = True
        elif a in d_tail.keys():
            nodes = [d_tail[a], a] + nodes
            d_head.pop(d_tail[a])
            d_tail.pop(a)
            added = True
        elif b in d_head.keys():
            nodes += [b, d_head[b]]
            d_tail.pop(d_head[b])
            d_head.pop(b)
            added = True
        elif b in d_tail.keys():
            nodes += [b, d_tail[b]]
            d_head.pop(d_tail[b])
            d_tail.pop(b)
            added = True

        if not added:
            nodes = [nodes[-1]] + nodes[:-1]
            genome.append(cycle_to_chromosome(nodes))
            nodes = []

    if nodes:
        nodes = [nodes[-1]] + nodes[:-1]
        genome.append(cycle_to_chromosome(nodes))

    # print("nodes", nodes)
    # print("genome", genome)
    return genome


if __name__ == "__main__":

    inp = "(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)"

    with open("dataset_8222_8.txt") as f:
        inp = f.read().splitlines()[0]

    a = "(2, 3), (4, 8), (5, 7), (6, 1)"
    b = "(3, 2), (4, 8), (5, 7), (6, 1)"

    for inp in (a, b):
        # convert input string to a list of tuples
        inp = inp[1:-1].split("), (")

        inp = [(int(i.split(", ")[0]), int(i.split(", ")[1])) for i in inp]

        genome = graph_to_genome(inp)
        print(genome)

        # format genome list into string
        for chromo in genome:

            fchromo = []

            for i, _ in enumerate(chromo):
                v = chromo[i]
                if v > 0:
                    fchromo.append("+" + str(v))
                else:
                    fchromo.append(str(v))

            print("(" + " ".join(fchromo) + ")", end="")

        print("")
