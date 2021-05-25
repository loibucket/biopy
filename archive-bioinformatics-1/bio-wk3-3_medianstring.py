import math


def ham_dist(p, q):
    """
    hamming distance is the number of mismatches between equal length sequences p and q
    returns integer
    """
    count = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            count += 1
    return count


def dee(pattern, seq):
    """
    find the min possible ham distance between a pattern and seq at all possible binding locations
    """
    k = len(pattern)
    d = math.inf
    for i in range(len(seq)-k+1):
        ham = ham_dist(pattern, seq[i:i+k])
        if ham < d:
            d = ham
    return d


def sumDee(pattern, dna):
    """
    sum the score for dna
    """
    sumD = 0
    for seq in dna:
        sumD += dee(pattern, seq)
    return sumD


def neighbors(pattern, d):
    """
    'mismatch-permutations'
    given a pattern, neighbors are all the possible permutation of patterns that have d or fewer mismatches
    recursive function
    returns a string of space-separated patterns
    """
    tides = set(["A", "C", "G", "T"])
    if d == 0:
        return set([pattern])
    if len(pattern) == 1:
        return tides
    neighborhood = set([])
    suffix_neighbors = neighbors(pattern[1:], d)
    for text in suffix_neighbors:
        if ham_dist(pattern[1:], text) < d:
            for tide in tides:
                neighborhood.add(tide+text)
        else:
            neighborhood.add(pattern[0]+text)
    return neighborhood


def medianString(dna, k):
    """
    the kmer with the lowest sum d across the dna
    """
    score = math.inf
    median = ""
    medlist = []
    kmers = neighbors('A'*k, k)
    for pattern in kmers:
        if sumDee(pattern, dna) < score:
            score = sumDee(pattern, dna)
            median = pattern

    for pattern in kmers:
        if sumDee(pattern, dna) == score:
            medlist.append(pattern)
    return medlist


if __name__ == "__main__":

    print(dee("AAA", "ATGCCAA"))
    print(sumDee("AAA", ["ATGCCAA", "ATGCCAA"]))
    print(neighbors("AAA", 3))

    k = 3
    dna = [
        "AAATTGACGCAT",
        "GACGACCACGTT",
        "CGTCAGCGCCTG",
        "GCTGAGCACCGG",
        "AGTTCGGGACAG"
    ]

    print(medianString(dna, k))

    k = 6
    dna = [
        "TTGGACCGAAATCCGTGTTTCCAAGACGAAATTTTACTGAGA",
        "CTTCAGCGCACATGACGACACACTATGAGACTCAGATCTTCA",
        "CTCGACGCTAGGCTGAAAGTCAAGGAAGGGCTCAGAGTAAAT",
        "GTTCCTCCGGTAAGGGGACTCTAACTCAGATCTGCCCTACCG",
        "ATTACTCTTGACAGGTAACGATGTCCTCCTGGTGCGCTCAGA",
        "TTGGAGTGTCGTGTCCACTCGAGCCTTAGACACGATGCCTGG",
        "CTGAGAAGCAGATCCGACGGAGGCCTCAACTCACGCTTACCG",
        "GTCTGGATTATCCTAAGAAAATGATTCTGAGAGCGGTTTGCG",
        "CCTGCCGACCCTTAGACAACTCGTCTCAGATGCTTGCTTACG",
        "GTTGGCAGATAGACGTAACTAAGAATTAGCTTTAAGGCTTAC"
    ]

    print(medianString(dna, k))

    k = 7
    dna = [
        "CTCGATGAGTAGGAAAGTAGTTTCACTGGGCGAACCACCCCGGCGCTAATCCTAGTGCCC",
        "GCAATCCTACCCGAGGCCACATATCAGTAGGAACTAGAACCACCACGGGTGGCTAGTTTC",
        "GGTGTTGAACCACGGGGTTAGTTTCATCTATTGTAGGAATCGGCTTCAAATCCTACACAG"
    ]

    print(medianString(dna, k))
