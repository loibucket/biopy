from collections import defaultdict
from heapq import nlargest


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


def immediate_neighbors(pattern):
    """
    given a pattern, immediate_neighbors are all the possible permutation of patterns that have 1 or fewer mismatches
    returns a string of space-separated patterns
    """
    tides = set(["A", "T", "C", "G"])
    neighborhood = set([pattern])
    for i in range(1, len(pattern)):
        symbol = pattern[i]
        tides.remove(symbol)
        for tide in tides:
            neighbor = pattern
            neighbor[i] = tide
            neighborhood.add(neighbor)
    return " ".join(list(neighborhood))


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


def freq_kmers(seq, k, d):
    """
    k-mer patterns with the most frequent matches to a given sequence
    pattern matches can have up to d nucleotide mismatches    
    """
    patterns = []
    def def_value(): return 0
    freqMap = defaultdict(def_value)
    n = len(seq)
    for i in range(n-k+1):
        pattern = seq[i:i+k]
        neighborhood = neighbors(pattern, d)
        for n in neighborhood:
            freqMap[n] += 1
    m = max(freqMap.values())
    for p in freqMap:
        if freqMap[p] == m:
            patterns.append(p)
    patterns.sort()
    return " ".join(patterns)


def complement(seq):
    """
    reverse complement of a sequence, which is the other strand the seq binds to
    """
    dct = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }
    mer = ""
    for char in seq:
        mer = dct[char] + mer
    return mer


def freq_rc_kmers(seq, k, d):
    """
    k-mer patterns with the most frequent matches to a given sequence
    pattern matches can have up to d nucleotide mismatches
    occurences of each pattern and its complement (e.g. 'ATCG' and 'CGAT') are counted together
    """
    patterns = []
    p_count = []
    def def_value(): return 0
    freqMap = defaultdict(def_value)
    n = len(seq)
    print("seq length", n)
    for i in range(n-k+1):
        if i % 10000 == 0:
            print(i)
        pattern = seq[i:i+k]
        neighborhood = neighbors(pattern, d)
        for n in neighborhood:
            freqMap[n] += 1
    freqMapRc = dict()
    for mer in freqMap:
        if complement(mer) in freqMap:
            freqMapRc[mer] = freqMap[mer] + freqMap[complement(mer)]
        else:
            freqMapRc[mer] = freqMap[mer]
    highest = nlargest(10, freqMapRc, key=freqMapRc.get)
    for h in highest:
        print(h, freqMapRc[h])

    m = max(freqMapRc.values())
    for p in freqMapRc:
        if freqMapRc[p] == m:
            patterns.append(p)
            p_count.append(freqMapRc[p])
    patterns.sort()
    return " ".join(patterns)


if __name__ == "__main__":

    # sample = [
    #     #("ACG", 1),
    #     ("GGCCCAGAG", 3),
    #     #("TGCCAGCCGCTA", 3),
    # ]

    # with open("Neighbors.txt", "r") as f:
    #     lst = f.read().splitlines()
    #     lst.sort()
    #     # print("\n".join(lst))

    # for s in sample:
    #     nb = list(neighbors(*s))
    #     nb.sort()
    #     # print("\n".join(nb))

    # for i, _ in enumerate(lst):
    #     if lst[i] != nb[i]:
    #         print(lst[i] + " " + nb[i])
    #     else:
    #         print("match")

    print('neighbors("ACGT", 3)', neighbors("ACGT", 3))
    print('len(neighbors("ACGT", 3))', len(neighbors("ACGT", 3)))

    sample = [
        ("ACGTTGCATGTCGCATGATGCATGAGAGCT", 4, 1),
        (complement("ACGTTGCATGTCGCATGATGCATGAGAGCT"), 4, 1),
        ("GCAGGCAGAATCAGCAGCAGAGCATTGTTGTGCAGGCAGTGTTGTAGCAAGCATGTAATCTTGTAGCAAGCAAATCGCAGAATCGCAGTGTAGCATGTTGTAGCAAGCATGTAATCTGTAGCATTGTGCAGAGCAAGCATTGTTGTTTGTGCAGAGCATTGTAATCTGTAGCAGCAGTGTTTGTTTGTTTGTTTGTGCAGGCAGAATCAATCTGTAGCATGTAATCGCAGTGTTTGTAATCTGTAGCATTGTTTGTGCAGGCAGTGTAGCAAATCAGCAGCAGAATCAATCTGTTGTAGCAAATCAATCGCAGGCAGTTGTTTGTTGTTGTAGCAAGCAAGCAAGCATTGTAGCAGCAGTTGTGCAGTGTGCAGTGTGCAGAGCA", 7, 2),
    ]

    for s in sample:
        print('freq_kmers(*s)', freq_kmers(*s))

    sample = [
        ("ACGT", 4, 3),
        ("AAAAAAAAAA", 2, 1),
        ("AGTCAGTC", 4, 2),
        ("AATTAATTGGTAGGTAGGTA", 4, 0),
        ("TAGCG", 2, 1),
        ("CGTGCGTTCTTCGGAACGGTTCTGGGTTCAACCGAACGGTGAACAACGGCGGGAACGGTGGGTGGGAACCGGGGGTTCCGCGCGGGTGTTCCGCGGGGGGGTTCTGGGTGCGAACCGGGAACGGCGGGGGTTCGGAACTTCTTCAACTGTTCTGTGGGGGAACGGTGCGGGCGTTCAACTTCTTCCGTTCGGAACTTCAACTGAACTTCGGCGGGTGCGTTCTGTTCAACCG", 6, 3),
    ]

    for s in sample:
        print('freq_rc_kmers(*s)', freq_rc_kmers(*s))
