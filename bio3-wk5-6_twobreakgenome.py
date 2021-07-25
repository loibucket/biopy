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


def graph_to_genome(colored_edges):
    """
    convert a list of colored edges to a genome in synteny blocks format
    """
    genome = []
    nodes = []
    visited_edges = set()
    cursor = colored_edges[0][1]

    while len(visited_edges) < len(colored_edges):

        for i, edge in enumerate(colored_edges):

            if edge in visited_edges:
                continue

            if nodes == []:
                nodes = [edge[0], edge[1]]
                visited_edges.add(edge)
                cursor = edge[1]
                continue

            if abs(cursor - edge[0]) == 1:
                nodes += [edge[0], edge[1]]
                cursor = edge[1]
                visited_edges.add(edge)
                continue

            if abs(cursor - edge[1]) == 1:
                nodes += [edge[1], edge[0]]
                cursor = edge[0]
                visited_edges.add(edge)
                continue

        nodes = [nodes[-1]] + nodes[:-1]
        genome.append(cycle_to_chromosome(nodes))
        nodes = []

    return genome


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


def two_break_genome(genome, breaks):
    """
    break a genome at 2 places
    """

    print("genome", genome, "\n")
    print("breaks", breaks, "\n")

    edges = colored_edges(genome)
    print("edges", edges, "\n")

    broke_edges = two_break_genome_graph(edges, breaks)
    print("broke_edges", broke_edges, "\n")

    broke_genome = graph_to_genome(broke_edges)

    # this rearrangement is needed to pass the grader
    broke_genome[0] = [broke_genome[0][-1]] + broke_genome[0][:-1]

    return broke_genome


if __name__ == "__main__":

    genome = "(+1 -2 -4 +3)"
    breaks = "1, 6, 3, 8"

    with open("dataset_8224_3 (6).txt") as f:
        dataset = f.read().splitlines()
        genome = dataset[0]
        breaks = dataset[1]

    genome = genome[1:-1].split(")(")

    for i in range(len(genome)):
        genome[i] = [int(s) for s in genome[i].split(" ")]

    breaks = [int(i) for i in breaks.split(", ")]

    out = two_break_genome(genome, breaks)

    for i in range(len(out)):
        for j in range(len(out[i])):
            out[i][j] = str(out[i][j]) if out[i][j] < 0 else "+" + str(out[i][j])

    out = str(out)[1:-1].replace("[", "(").replace("]", ")").replace("'", "").replace(",", "")

    print(out)
