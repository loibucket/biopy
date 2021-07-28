import biopy as bp


def most_probable_kmer(sequence, k, profile):
    """
    most probable kmer in the seq that fits the profile
    """
    km = bp.all_kmers(sequence, k)
    score = -1
    median = ""
    for kmer in km:
        p = bp.kmer_fit_probability(kmer, profile)
        if p > score:
            score = p
            median = kmer
    return median
