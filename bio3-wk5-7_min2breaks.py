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


def cycles(p, q):
    """
    get the number of cycle node groups formed by the colored edges of p and q
    """
    all_edges = set(colored_edges(p) + colored_edges(q))

    cycle_list = []
    cycle = set()

    while all_edges:
        changes = 0

        if not cycle:
            edge = min(all_edges)
            cycle.add(edge[0])
            cycle.add(edge[1])
            changes += 1
            all_edges.remove(edge)

        clear_edges = []
        for (a, b) in all_edges:
            if a in cycle or b in cycle:
                cycle.add(a)
                cycle.add(b)
                changes += 1
                clear_edges.append((a, b))

        for edge in clear_edges:
            all_edges.remove(edge)

        if changes == 0:
            cycle_list.append(list(cycle))
            cycle = set()

    if cycle:
        cycle_list.append(list(cycle))

    return cycle_list


if __name__ == "__main__":

    p = "(+1 +2 +3 +4 +5 +6)"
    q = "(+1 -3 -6 -5)(+2 -4)"

    with open("dataset_288_4.txt") as f:
        data = f.read().splitlines()

    p = data[0]
    q = data[1]

    blocks = p[1:-1].replace(")(", " ").split()
    print("blocks", blocks[:10], "...", len(blocks))

    p = p[1:-1].split(")(")
    q = q[1:-1].split(")(")

    for genome in [p, q]:
        for i in range(len(genome)):
            genome[i] = [int(s) for s in genome[i].split(" ")]

    print("p", p[0][:10], "...", len(p))
    print("q", q[0][:10], "...", len(q))

    cyc = cycles(p, q)
    print("cycles", cyc[0][:10], "...", len(cyc))

    print(len(blocks) - len(cyc))
