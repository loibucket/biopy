from collections import defaultdict


def def_value():
    return 0


def motifs_score(motifs):
    """
    get score of motifs
    """
    score = 0
    for i in range(len(motifs[0])):
        dct = defaultdict(def_value)
        for m in motifs:
            dct[m[i]] += 1
        lst = [dct["A"], dct["C"], dct["T"], dct["G"]]
        lst.sort()
        score += lst[0] + lst[1] + lst[2]
    return score
