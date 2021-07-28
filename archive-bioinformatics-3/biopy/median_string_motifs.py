import biopy as bp
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


def min_ham_dist_helper(pattern, seq):
    """
    find the min possible ham distance between a pattern and seq at all possible binding locations
    """
    k = len(pattern)
    dist = math.inf
    candidates = set()
    for i in range(len(seq)-k+1):
        compare = seq[i:i+k]
        ham = ham_dist(pattern, compare)
        if ham < dist:
            dist = ham
            candidates = set([compare])
        elif ham == dist:
            candidates.add(compare)
    return dist, list(candidates)


def min_ham_dist(pattern, dna):
    """
    sum the score for dna
    """
    dist = 0
    candidates = []
    for seq in dna:
        a, b = min_ham_dist_helper(pattern, seq)
        dist += a
        candidates.append(b)
    return dist, candidates


def median_string_motifs(dna, k):
    """
    the motifs made from kmers with the lowest sum d across the dna
    """
    min_d = math.inf
    median_candidates = {}
    kmers = set()
    for seq in dna:
        kmers |= set(bp.all_kmers(seq, k))
    for pattern in kmers:
        dist, c = min_ham_dist(pattern, dna)
        if dist < min_d:
            min_d = dist
            median_candidates = {}
            median_candidates[pattern] = c
        elif dist == min_d:
            median_candidates[pattern] = c
    return dist, median_candidates
