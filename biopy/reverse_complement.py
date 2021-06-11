def reverse_complement(seq):
    """
    reverse complement of a sequence, which is the other strand the seq binds to
    """
    dct = {
        "A": "T",
        "T": "A",
        "C": "G",
        "G": "C"
    }
    mer = ""
    for char in seq:
        mer = dct[char] + mer
    return mer
