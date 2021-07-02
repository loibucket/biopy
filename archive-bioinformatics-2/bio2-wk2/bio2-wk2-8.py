import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp

with open("wk2quiz3a.txt") as dataset:
    pairs = dataset.read().splitlines()
    print(pairs)
    seq = bp.ord_pairs_to_sequence(4, 2, pairs, debug=True)
    print(seq)
