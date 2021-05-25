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


def kmers_in_seq(seq, k, d):
    """
    all the kmer patterns found in seq, with up to d mismatches
    """
    kmers = set()
    for i in range(0, len(seq)-k+1):
        kmers.add(seq[i:i+k])
    if d == 0:
        return kmers
    nmers = set()
    for kmer in kmers:
        nmers |= neighbors(kmer, d)
    return nmers


def dna_has_mer(dna, mer, d):
    """
    does a set of dna sequences contain the pattern mer, with up to d mismatches
    """
    for seq in dna:
        min_ham = float("inf")
        for kmer in kmers_in_seq(seq, len(mer), 0):
            min_ham = min(min_ham, ham_dist(mer, kmer))
        if min_ham > d:
            return False
    return True


def motif_enumeration(dna, k, d):
    """
    what kmers are found in all seq in the dna set, max d mismatches allowed
    """
    patterns = set()
    kmers = set()
    # get all possible kmers
    for seq in dna:
        # set join
        kmers |= kmers_in_seq(seq, k, d)
    for kmer in kmers:
        if dna_has_mer(dna, kmer, d):
            patterns.add(kmer)
    p = list(patterns)
    p.sort()
    return p


if __name__ == "__main__":

    print("kmer_in_seq", kmers_in_seq("ACTGCGCTCGATCGAT", 3, 0))
    print("kmer_in_seq", kmers_in_seq("ACTGCGCTCGATCGAT", 3, 1))
    print("dna_has_mer", dna_has_mer(["AAACCC", "AAACTT"], "AC", 1))
    print("dna_has_mer", dna_has_mer(["AAAGCC", "AAACTT"], "AC", 1))
    print("dna_has_mer", dna_has_mer(["AAAGCC", "AAACTT"], "ACC", 0))
    print("dna_has_mer", dna_has_mer(["AAAGCC", "AAACTT"], "ACC", 1))

    with open("dataset_156_8.txt", "r") as f:
        lines = f.read().splitlines()
        (k, d) = lines[0].split(" ")
        k = int(k)
        d = int(d)
        dna = lines[1:]

    print(k, d, dna)
    print(" ".join(motif_enumeration(dna, k, d)))
