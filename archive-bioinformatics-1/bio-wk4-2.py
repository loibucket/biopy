import sys
import random
import math

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


def def_value():
    return 0


def def_list():
    return []


def gibbs_sampler(dna, k, t, n):
    # start with a random motif
    test_motifs = []
    for ith in range(t):
        s = random.randint(0, len(dna[ith]) - k)
        test_motifs.append(dna[ith][s : s + k])
    best_motifs = test_motifs.copy()
    best_score = bp.motifs_score(test_motifs)
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
        s = bp.motifs_score(test_motifs)
        if s < best_score:
            best_motifs = test_motifs.copy()
            best_score = s
    return best_motifs


def iter_gibbs_sampler(dna, k, t, n, iter):
    best_motifs = []
    best_score = math.inf
    for cnt in range(iter):
        print("cnt", cnt)
        test_motifs = gibbs_sampler(dna, k, t, n)
        s = bp.motifs_score(test_motifs)
        if s < best_score:
            best_score = s
            best_motifs = test_motifs.copy()
    return best_motifs


if __name__ == "__main__":

    # datasets = [["dataset_wk4-2.txt", "dataset_wk4-2a.txt"]]
    datasets = [["datasets/dataset_163_4.txt"]]
    for d in datasets:
        with open(d[0], "r") as f:
            lines = f.read().splitlines()
            (k, t, n) = [int(x) for x in lines[0].split(" ")]
            dna = lines[1 : t + 1]

        out = iter_gibbs_sampler(dna, k, t, n, 20)
        print("\n".join(out))
        print(bp.motifs_score(out))

        file = open("out.txt", "w")
        file.write("\n".join(out))
        file.close()

        if len(d) > 1:
            with open(d[1], "r") as f:
                lines = f.read().splitlines()
                lines.sort()
                print("\n".join(lines))
                print(bp.motifs_score(lines))
                print(out == lines)
