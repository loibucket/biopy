from collections import defaultdict


def def_value():
    return 1


def def_list():
    return []


def laplace_profile(motifs):
    """
    get the profile of motifs
    """
    d = len(motifs) + 4
    pro = defaultdict(def_list)
    for i in range(len(motifs[0])):
        dct = defaultdict(def_value)
        for m in motifs:
            dct[m[i]] += 1
        pro["A"].append(dct["A"] / d)
        pro["C"].append(dct["C"] / d)
        pro["G"].append(dct["G"] / d)
        pro["T"].append(dct["T"] / d)
    return pro
