import biopy as bp


def patterns_to_sequence(patterns, debug=False):
    """
    reconstruct a sequence from a set of patterns, (a kmers list)
    """
    adjacency_list = bp.debrujin_graph(patterns)
    euler = bp.euler_cycle(adjacency_list, debug)[0]
    # start with the first kmer
    seq = euler[0]
    # add the last char from each following kmer
    for kmer in euler[1:]:
        seq += kmer[-1]
    return seq
