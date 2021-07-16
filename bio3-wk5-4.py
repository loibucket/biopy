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


def graph_to_genome(colored_edges):
    """
    convert a ordered list of colored edges to a genome in synteny blocks format
    """
    genome = []

    nodes = [colored_edges[0][0], colored_edges[0][1]]

    for edge in colored_edges[1:]:

        if nodes == []:
            nodes = [edge[0], edge[1]]
            continue

        nodes += [edge[0], edge[1]]

        if edge[1] == nodes[0] + 1 or edge[1] == nodes[0] - 1:
            if nodes[-1] != nodes[-2] + 1 and nodes[-1] != nodes[-2] - 1:
                nodes = [nodes[-1]] + nodes[:-1]
            genome.append(cycle_to_chromosome(nodes))
            nodes = []

    return genome


if __name__ == "__main__":

    inp = "(2, 4), (3, 6), (5, 1), (7, 9), (10, 12), (11, 8)"

    with open("dataset_8222_8.txt") as f:
        inp = f.read().splitlines()[0]

    # convert input string to a list of tuples
    inp = inp[1:-1].split("), (")

    inp = [(int(i.split(", ")[0]), int(i.split(", ")[1])) for i in inp]

    genome = graph_to_genome(inp)

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
