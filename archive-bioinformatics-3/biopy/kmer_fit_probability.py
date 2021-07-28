def kmer_fit_probability(mer, profile):
    """
    calculate probability of mer fitting into profile
    """
    prob = 1
    for i, char in enumerate(mer):
        prob *= profile[char][i]
    return prob
