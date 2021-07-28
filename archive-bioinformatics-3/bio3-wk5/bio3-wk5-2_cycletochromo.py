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


if __name__ == "__main__":

    inp = [1, 2, 4, 3, 6, 5, 7, 8]

    with open("dataset_8222_5 (1).txt") as f:
        inp = [int(i) for i in f.read().splitlines()[0][1:-1].split()]

    out = cycle_to_chromosome(inp)

    fout = []

    for o in out:
        if o > 0:
            fout.append("+" + str(o))
        else:
            fout.append(str(o))

    print("(" + " ".join(fout) + ")")
