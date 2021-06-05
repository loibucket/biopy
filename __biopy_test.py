import biopy as bp

if __name__ == "__main__":

    motifs = [
        "TCGGGGGTTTTT",
        "CCGGTGACTTAC",
        "ACGGGGATTTTC",
        "TTGGGGACTTTT",
        "AAGGGGACTTCC",
        "TTGGGGACTTCC",
        "TCGGGGATTCAT",
        "TCGGGGATTCCT",
        "TAGGGGAACTAC",
        "TCGGGTATAACC"
    ]

    print(bp.entropy(motifs))
    print(9.916)

    seq = "TCGGGGGTTTTT"
    print(bp.kmers(seq, 4))

    motifs = [
        "TAAC",
        "GTCT",
        "ACTA",
        "AGGT"
    ]
    print(bp.laplace_profile(motifs))
    print({'A': [0.375, 0.25, 0.25, 0.25], 'C': [0.125, 0.25, 0.25, 0.25], 'G': [0.25, 0.25, 0.25, 0.125], 'T': [0.25, 0.25, 0.25, 0.375]})

    pattern = "ACGGGGATTACC"
    profile = {'A': [.2, .2, 0, 0, 0, 0, .9, .1, .1, .1, .3, 0],
               'C': [.1, .6, 0, 0, 0, 0, 0, .4, .1, .2, .4, .6],
               'G': [0, 0, 1, 1, .9, .9, .1, 0, 0, 0, 0, 0],
               'T': [.7, .2, 0, 0, .1, .1, 0, .5, .8, .7, .3, .4]}

    print(bp.prob_fit(pattern, profile))
    print(0.000839808)

    profile = {
        'A': [0.2, 0.2, 0.3, 0.2, 0.3],
        'C': [0.4, 0.3, 0.1, 0.5, 0.1],
        'G': [0.3, 0.3, 0.5, 0.2, 0.4],
        'T': [0.1, 0.2, 0.1, 0.1, 0.2]
    }

    print(bp.profile_most_probable("ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT", 5, profile))
    print("CCGAG")

    motifs = [
        "TCGGGGGTTTTT",
        "CCGGTGACTTAC",
        "ACGGGGATTTTC",
        "TTGGGGACTTTT",
        "AAGGGGACTTCC",
        "TTGGGGACTTCC",
        "TCGGGGATTCAT",
        "TCGGGGATTCCT",
        "TAGGGGAACTAC",
        "TCGGGTATAACC"
    ]
    print(bp.score(motifs))
    print(30)
