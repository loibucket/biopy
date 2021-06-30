import biopy as bp

with open("wk2quiz3a.txt") as dataset:
    pairs = dataset.read().splitlines()
    print(pairs)
    seq = bp.ord_pairs_to_sequence(pairs, 4, 2, debug=True)
    print(seq)
