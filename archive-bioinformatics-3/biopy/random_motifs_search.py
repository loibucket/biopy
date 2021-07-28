import random
import biopy as bp
import math


def random_motifs_search(dna, k, n=100, repeat=20):
    best_score = math.inf
    best_motifs = []

    for _ in range(repeat):
        (score, motifs) = random_motifs_search_helper(dna, k, n)
        if score < best_score:
            best_score = score
            best_motifs = motifs

    return best_score, best_motifs


def random_motifs_search_helper(dna, k, n):
    """
    find motifs of length k
    """
    best_motifs = []
    best_score = math.inf
    for i in range(len(dna)):
        s = random.randint(0, len(dna[i]) - k)
        best_motifs.append(dna[i][s:s + k])

    for i in range(n):
        better_motifs = bp.most_probable_motifs(dna, bp.laplace_profile(best_motifs))
        s = bp.score(better_motifs)
        if s < best_score:
            best_motifs = better_motifs.copy()
            best_score = s
        else:
            return best_score, best_motifs
