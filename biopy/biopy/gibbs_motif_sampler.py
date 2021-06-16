import random
import biopy as bp
import math


def gibbs_motif_sampler(dna, k, n=100, repeat=20):

    best_score = math.inf
    best_motifs = []

    for _ in range(repeat):
        (score, motifs) = gibbs_sampler_helper(dna, k, n)
        if score < best_score:
            best_score = score
            best_motifs = motifs

    return best_score, best_motifs


def gibbs_sampler_helper(dna, k, n):
    # start with a random motif
    t = len(dna)
    test_motifs = []
    for ith in range(t):
        s = random.randint(0, len(dna[ith]) - k)
        test_motifs.append(dna[ith][s:s + k])
    best_motifs = test_motifs.copy()
    best_score = bp.score(test_motifs)
    for _ in range(n):
        # take out a random string in motifs, calc profile of result
        rand = random.randint(0, t - 1)
        del test_motifs[rand]
        p = bp.laplace_profile(test_motifs)
        # replace the string that was removed
        kmers = bp.all_kmers(dna[rand], k)
        weights = []
        for kmer in kmers:
            weights.append(bp.kmer_fit_probability(kmer, p))
        chosen = random.choices(kmers, weights=weights, k=1)[0]
        test_motifs.insert(rand, chosen)
        # compare scores
        s = bp.score(test_motifs)
        if s < best_score:
            best_motifs = test_motifs.copy()
            best_score = s
    return (best_score, best_motifs)
