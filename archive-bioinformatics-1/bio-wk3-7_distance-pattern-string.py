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


def kmers(seq, k):
    """
    find all the kmers in seq
    """
    kmers = []
    for i in range(len(seq)-k+1):
        kmers.append(seq[i:i+k])
    return list(dict.fromkeys(kmers))  # removes duplicates


def distance_pattern_strings(pattern, dna):
    """
    sum of min ham dist between pattern and each dna
    """
    k = len(pattern)
    distance = 0
    for seq in dna:
        min_ham_dist = math.inf
        for kmer in kmers(seq, k):
            ham_d = ham_dist(pattern, kmer)
            if min_ham_dist > ham_d:
                min_ham_dist = ham_d
        distance += min_ham_dist
    return distance


if __name__ == "__main__":

    with open("dataset_5164_1.txt", "r") as f:
        lines = f.read().splitlines()
        pattern = lines[0]
        dna = lines[1].split(" ")
        print(pattern, dna)
    print(distance_pattern_strings(pattern, dna))
