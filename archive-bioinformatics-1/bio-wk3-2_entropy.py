from collections import defaultdict
from math import log


def def_value():
    return 0


def entropy(motifs):
    d = len(motifs) * 1.0
    print(d)
    entropy = 0
    for i in range(len(motifs[0])):
        dct = defaultdict(def_value)
        for m in motifs:
            dct[m[i]] += 1
        a = dct["A"]/d * log(max(dct["A"]/d, 0.000001), 2)
        c = dct["C"]/d * log(max(dct["C"]/d, 0.000001), 2)
        t = dct["T"]/d * log(max(dct["T"]/d, 0.000001), 2)
        g = dct["G"]/d * log(max(dct["G"]/d, 0.000001), 2)
        entropy += (a+c+t+g)*(-1)
    return entropy


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

    print(entropy(motifs))

    print(0.5*log(0.5, 2) + 0.5*log(0.5, 2))
    print(0.25*log(0.25, 2)*4)
    print(1*log(1, 2))
    print(0.25*log(0.25, 2) + 0.5*log(0.5, 2) + 0.25*log(0.25, 2))
