import numpy as np


def score_from_file(file):
    """
    build a map of pair scores from file
    """
    with open("blosum62.txt") as file:
        lines = file.read().splitlines()

        chars = lines[0].split()

        score_key = {}

        for l in lines[1:]:
            linevals = l.split()
            for i, s in enumerate(linevals[1:]):
                pair = sorted([linevals[0], chars[i]])
                score_key[":".join(pair)] = int(s)

        return score_key


def path_from_pair(v, w, indel, score_matrix):
    """
    given strings v and w, construct a path matrix
    """
    ## use y x coords for score (nodes), use i j coords for backtrack (paths)
    score = np.zeros((len(v) + 1, len(w) + 1), dtype=int)
    for y in range(1, len(v) + 1):
        score[y][0] = score[y - 1][0] + indel
    for x in range(1, len(w) + 1):
        score[0][x] = score[0][x - 1] + indel

    backtrack = np.full((len(v), len(w)), ".")
    directions = {0: "↓", 1: "→", 2: "↘"}

    for i in range(len(v)):
        for j in range(len(w)):
            pair = [v[i], w[j]]
            pair = ":".join(sorted(pair))
            y, x = i + 1, j + 1
            score_list = [score[y - 1][x] + indel, score[y][x - 1] + indel, score[y - 1][x - 1] + score_matrix[pair]]
            high_score = max(score_list)
            score[y][x] = high_score
            backtrack[i][j] = directions[score_list.index(high_score)]

    print("score\n", score)
    print("backtrack\n", backtrack)
    return score, backtrack


def back_path(backtrack, v, w, i, j):
    """
    output path created by backtrack
    """
    vv = list(v)
    ww = list(w)
    istring = []
    jstring = []
    while vv or ww:
        if backtrack[i][j] == "↓":
            istring = [vv.pop()] + istring
            jstring = ["-"] + jstring
            i -= 1
        elif backtrack[i][j] == "→":
            istring = ["-"] + istring
            jstring = [ww.pop()] + jstring
            j -= 1
        elif backtrack[i][j] == "↘":
            istring = [vv.pop()] + istring
            jstring = [ww.pop()] + jstring
            i -= 1
            j -= 1

    while vv:
        istring = [vv.pop()] + istring
        jstring = ["-"] + jstring
        i -= 1

    while ww:
        istring = ["-"] + istring
        jstring = [ww.pop()] + jstring
        j -= 1

    print("v", istring)
    print("w", jstring)
    return ["".join(istring), "".join(jstring)]


if __name__ == "__main__":

    score_matrix = score_from_file("blosum62.txt")
    print("score_matrix\n", score_matrix)

    v = "PLEASANTLY"
    w = "MEANLY"
    indel = -5
    node_scores, path_matrix = path_from_pair(v, w, indel, score_matrix)

    out = back_path(path_matrix, v, w, len(v) - 1, len(w) - 1)

    print(node_scores[-1][-1])
    for o in out:
        print("".join(o))
