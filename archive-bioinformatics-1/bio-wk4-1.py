from collections import defaultdict
import random
import copy
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


def most_pr(seq, k, profile):
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


def most_pr_motifs(dna, profile):
    """
    list of most probable motifs for dna
    """
    motifs = []
    for seq in dna:
        motifs.append(most_pr(seq, len(profile['A']), profile))
    return motifs


def random_motif_search(dna, k, t):
    """
    find motifs of length k
    """
    best_motifs = []
    for i in range(t):
        s = random.randint(0, len(dna[i])-k)
        best_motifs.append(dna[i][s:s+k])

    for i in range(2):
        print(i)
        better_motifs = most_pr_motifs(dna, pro(best_motifs))
        print(better_motifs, score(better_motifs))
        if score(better_motifs) < score(best_motifs):
            best_motifs = copy.deepcopy(better_motifs)
        else:
            return best_motifs


def iter_motif_search(dna, k, t, i):
    best_score = math.inf
    best_motifs = []
    for _ in range(i):
        m = random_motif_search(dna, k, t)
        s = score(m)
        if s < best_score:
            best_score = s
            best_motifs = m
    return best_motifs


if __name__ == "__main__":

    k = 3
    t = 4
    dna = [
        "ATGAGGTC",
        "GCCCTAGA",
        "AAATAGAT",
        "TTGTGCTA"
    ]

    motifs = ['GTC', 'CCC', 'ATA', 'GCT']

    print(" ".join(most_pr_motifs(dna, pro(motifs))))

    # datasets = [
    #     ["dataset_wk4-1.txt", "dataset_wk4-1a.txt"],
    #     ["dataset_wk4-1-2.txt", "dataset_wk4-1-2a.txt"],
    #     ["dataset_wk4-1-3.txt", "dataset_wk4-1-3a.txt"]
    # ]
    # datasets = [["dataset_161_5.txt", "x.txt"]]

    # for d in datasets:
    #     with open(d[0], "r") as f:
    #         lines = f.read().splitlines()
    #         (k, t) = [int(x) for x in lines[0].split(" ")]
    #         dna = lines[1:t+1]

    # out = iter_motif_search(dna, k, t, 1000)
    # print("\n".join(out))
    # print(score(out))

    # with open(d[1], "r") as f:
    #     lines = f.read().splitlines()
    #     lines.sort()
    #     print("\n".join(lines))
    #     print(score(lines))
    #     print(out == lines)
