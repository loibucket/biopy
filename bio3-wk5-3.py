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


if __name__ == "__main__":

    inp = "(+1 -2 -3)(+4 +5 -6)"

    with open("dataset_8222_7.txt") as f:
        inp = f.read().splitlines()[0]

    inp = inp[1:-1].split(")(")

    for i in range(len(inp)):
        inp[i] = [int(s) for s in inp[i].split(" ")]

    out = colored_edges(inp)

    print(out)
