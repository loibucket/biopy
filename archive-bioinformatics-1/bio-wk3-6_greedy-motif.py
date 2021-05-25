from collections import defaultdict
import math


def def_value():
    return 0


def def_list():
    return []


def score(motifs):
    """
    get score of motifs
    """
    score = 0
    for i in range(len(motifs[0])):
        dct = defaultdict(def_value)
        for m in motifs:
            dct[m[i]] += 1
        lst = [dct["A"], dct["C"], dct["T"], dct["G"]]
        lst.sort()
        score += lst[0]+lst[1]+lst[2]
    return score


def pro(motifs):
    """
    get the profile of motifs
    """
    d = len(motifs) * 1.0
    pro = defaultdict(def_list)
    for i in range(len(motifs[0])):
        dct = defaultdict(def_value)
        for m in motifs:
            dct[m[i]] += 1/d
        pro["A"].append((dct["A"] or 0)+1/d)
        pro["C"].append((dct["C"] or 0)+1/d)
        pro["G"].append((dct["G"] or 0)+1/d)
        pro["T"].append((dct["T"] or 0)+1/d)
    return pro


def kmers(seq, k):
    """
    find all the kmers in seq
    """
    kmers = []
    for i in range(len(seq)-k+1):
        kmers.append(seq[i:i+k])
    return list(dict.fromkeys(kmers))  # removes duplicates


def pr(mer, profile):
    """
    calculate probability of mer fitting into profile
    """
    prob = 1
    for i, char in enumerate(mer):
        prob *= profile[char][i]
    return prob


def mostPr(seq, k, profile):
    """
    most probable kmer in the seq that fits the profile
    """
    km = kmers(seq, k)
    score = -1
    median = ""
    for kmer in km:
        p = pr(kmer, profile)
        if p > score:
            score = p
            median = kmer
    return median


def greedyMotifSearch(dna, k, t):
    """
    best motif among the dna
    """
    bestScore = math.inf

    for i in range(len(dna[0])-k+1):
        motif = [dna[0][i:i+k]]
        for j in range(1, t):
            motif.append(mostPr(dna[j], k, pro(motif)))
        if score(motif) < bestScore:
            bestScore = score(motif)

    bestList = []
    for i in range(len(dna[0])-k+1):
        motif = [dna[0][i:i+k]]
        for j in range(1, t):
            motif.append(mostPr(dna[j], k, pro(motif)))
        if score(motif) == bestScore:
            bestList.append(motif)

    return bestList


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

    # print(score(motifs))
    # print(pro(motifs))

    k = 3
    t = 5
    dna = [
        "GGCGTTCAGGCA",
        "AAGAATCAGTCA",
        "CAAGGAGTTCGC",
        "CACGTCAATCAC",
        "CAATAATATTCG"
    ]

    print((greedyMotifSearch(dna, k, t)))

    with open("dataset_160_9.txt", "r") as f:
        lines = f.read().splitlines()
        (k, t) = [int(x) for x in lines[0].split(" ")]
        dna = lines[1:t+1]

    print((greedyMotifSearch(dna, k, t)))

    k = 7
    t = 3
    dna = [
        "CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC",
        "GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC",
        "GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG"
    ]

    print((greedyMotifSearch(dna, k, t)))
