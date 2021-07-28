import copy


def chromosome_to_cycle(chromosome):
    """
    convert genome to graph, where
    node1 = chrom1_head, node2 = chrom1_tail
    node3 = chrom2_head, node4 = chrom2_tail
    """
    nodes = [0] * (len(chromosome) * 2 + 1)
    chromo = [0] + chromosome.copy()
    for j in range(1, len(chromo)):
        i = chromo[j]
        if i > 0:
            nodes[2 * j - 1] = 2 * i - 1
            nodes[2 * j] = 2 * i
        else:
            nodes[2 * j - 1] = -2 * i
            nodes[2 * j] = -2 * i - 1
    return nodes[1:]


def colored_edges(genome):
    """
    find the colored edges of a genome, in node format
    """
    edges = []
    for chromo in genome:
        nodes = [0] + chromosome_to_cycle(chromo)
        nodes.append(nodes[1])
        for j in range(1, len(chromo) + 1):
            edges.append((nodes[2 * j], nodes[2 * j + 1]))

    return edges


def two_break_genome_graph(graph, breaks):
    """
    transform a genome graph with the given breaks
    """

    i1 = breaks[0]
    i2 = breaks[1]
    i3 = breaks[2]
    i4 = breaks[3]

    new_g = copy.deepcopy(graph)

    for i in range(len(graph)):

        compare = graph[i]

        if compare == (i1, i2):
            new_g[i] = (i4, i2)
            continue

        if compare == (i2, i1):
            new_g[i] = (i2, i4)
            continue

        if compare == (i3, i4):
            new_g[i] = (i3, i1)
            continue

        if compare == (i4, i3):
            new_g[i] = (i1, i3)
            continue

    return new_g


def cycle_to_chromosome(nodes):
    """
    convert a chromosome in ordered nodes format to synteny blocks format
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
    convert an order-independent list of colored edges to a genome in synteny blocks format
    """
    colored_edges = copy.deepcopy(edges_graph)

    d_head = dict()
    d_tail = dict()

    for edge in colored_edges:
        d_head[edge[0]] = edge[1]
        d_tail[edge[1]] = edge[0]

    genome = []
    nodes = []

    while d_head:

        if nodes == []:
            key = next(iter(d_head))
            nodes = [key, d_head[key]]
            d_tail.pop(d_head[key])
            d_head.pop(key)
            continue

        a = nodes[0] - 1 if nodes[0] % 2 == 0 else nodes[0] + 1
        b = nodes[-1] - 1 if nodes[-1] % 2 == 0 else nodes[-1] + 1

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

    return genome


def breaksort(p, q):
    """
    get a sequence of genomes formed by 2-breaks, that turns p into q
    """
    p_edges = colored_edges(p)
    q_edges = colored_edges(q)
    print("p_edges", p_edges)
    print("q_edges", q_edges, "\n")

    int_g = p.copy()
    int_edges = copy.deepcopy(p_edges)

    steps = [p.copy()]
    loop = 0
    finished = False
    while not finished:
        loop += 1
        if loop > 99:
            print("loop break")
            break
        print("int_edges", int_edges, "int_g", int_g)
        breaks = []
        finished = True
        for blue in q_edges:
            if blue not in int_edges and (blue[1], blue[0]) not in int_edges:
                finished = False
                a = blue[0]
                b = blue[1]
                breaks = []
                for red in int_edges:
                    if a == red[0] or b == red[0]:
                        breaks += [red[1]]
                    if a == red[1] or b == red[1]:
                        breaks += [red[0]]

                if (breaks[0], a) in int_edges or (a, breaks[0]) in int_edges:
                    breaks = [breaks[0], a, breaks[1], b]
                else:
                    breaks = [breaks[1], a, breaks[0], b]

                print("blue_edge", blue, "breaks", breaks, "\n")
                int_edges = two_break_genome_graph(int_edges, breaks)
                int_g = graph_to_genome(int_edges)
                steps.append(int_g)
                break

    return steps


if __name__ == "__main__":

    p = "(+1 -2 -3 +4)"
    q = "(+1 +2 -4 -3)"

    with open("dataset_288_5 (3).txt") as f:
        data = f.read().splitlines()

    p = data[0]
    q = data[1]

    blocks = p[1:-1].replace(")(", " ").split()

    p = p[1:-1].split(")(")
    q = q[1:-1].split(")(")

    for genome in [p, q]:
        for i in range(len(genome)):
            genome[i] = [int(s) for s in genome[i].split(" ")]

    steps = breaksort(p, q)
    print("\n", "steps", steps, "\n")

    for s in steps:
        for i, g in enumerate(s):
            s[i] = "(" + " ".join([str(c) if c < 0 else "+" + str(c) for c in g]) + ")"
        print("".join(s))
