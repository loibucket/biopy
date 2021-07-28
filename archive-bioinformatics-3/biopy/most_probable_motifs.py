import biopy as bp


def most_probable_motifs(dna, profile):
    """
    list of most probable motifs for dna
    """
    motifs = []
    for seq in dna:
        k = len(profile['A'])
        motifs.append(bp.most_probable_kmer(seq, k, profile))
    return motifs
