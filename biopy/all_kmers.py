def all_kmers(sequence, k):
    """
    find all the kmers in seq
    """
    kmers = []
    for i in range(len(sequence)-k+1):
        kmers.append(sequence[i:i+k])
    return list(dict.fromkeys(kmers))  # removes duplicates
    # return kmers
