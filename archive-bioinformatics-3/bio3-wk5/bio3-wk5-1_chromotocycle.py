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


if __name__ == "__main__":

    inp = [1, -2, -3, 4]

    with open("dataset_8222_4.txt") as f:
        inp = [int(i) for i in f.read().splitlines()[0][1:-1].split()]

    out = chromosome_to_cycle(inp)

    print("(" + " ".join([str(i) for i in out]) + ")")
