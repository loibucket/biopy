import biopy as bp


def print_out(dna, k):
    d, out = bp.median_string_motifs(dna, k)

    print(">best ham dist:", d)
    for m_string in out:
        print(">median string:", m_string)
        print(">motif candidates:")
        for line in out[m_string]:
            print(" ".join(line))

    for i, m_string in enumerate(out):
        motifs = []
        for line in out[m_string]:
            motifs.append(line[0])
        print(">median string:", m_string, "score:", bp.score(motifs))
        print("\n".join(motifs))
        write_motifs('motifs-median-'+str(i)+'.txt', motifs)

    score, motifs = bp.gibbs_motif_sampler(dna, k)
    print(">gibbs:", score)
    print("\n".join(motifs))
    write_motifs("motifs-median.txt", motifs)

    score, motifs = bp.random_motif_search(dna, k)
    print(">random:", score)
    print("\n".join(motifs))
    write_motifs("motifs-random.txt", motifs)


def write_motifs(fname, motifs):
    f = open(fname, 'w')
    f.write(str(bp.score(motifs))+"\n")
    f.write("\n".join(motifs))
    f.close()


if __name__ == "__main__":

    # test
    # k = 3

    # dna = [
    #     "AAATTGACGCAT",
    #     "GACGACCACGTT",
    #     "CGTCAGCGCCTG",
    #     "GCTGAGCACCGG",
    #     "AGTTCGGGACAG"
    # ]

    # print_out(dna, k)

    filename = "upstream250.txt"

    with open(filename, "r") as f:
        lines = f.read().splitlines()
        dna = []
        for i in range(1, len(lines), 2):
            dna.append(lines[i])

    # k = 20

    # print_out(dna, k)

    file = open('dna.txt', 'w')
    file.write("\n".join(dna))
    file.close()
