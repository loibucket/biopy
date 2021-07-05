"""
1.3 The Changing Faces of Sequence Alignment
Code Challenge: Solve the Overlap Alignment Problem.

Input: Two strings v and w, each of length at most 1000.
Output: The score of an optimal overlap alignment of v and w, followed by an alignment of a suffix v' of v and a prefix w' of w achieving this maximum score. Use an alignment score in which matches count +1 and both the mismatch and indel penalties are 2.
"""

import numpy as np
from numpy import unravel_index
import math


def path_from_pair(v, w, indel, mismatch, match):
    """
    given strings v and w, construct a path matrix
    """
    ## use y x coords for score matrix (nodes), use i j coords for backtrack matrix (paths)
    score = np.zeros((len(v) + 1, len(w) + 1), dtype=int)
    for x in range(1, len(w) + 1):
        score[0][x] = score[0][x - 1] + indel

    ## set scores for col 1
    for i in range(len(v)):
        if v[i] == w[0]:
            score[i][0] = 0
        else:
            score[i][0] = score[i - 1][0] + indel

    backtrack = np.full((len(v), len(w)), ".")
    directions = {0: "↓", 1: "→", 2: "↘"}

    for i in range(len(v)):
        for j in range(len(w)):
            m = match if v[i] == w[j] else mismatch
            y, x = i + 1, j + 1
            score_list = [score[y - 1][x] + indel, score[y][x - 1] + indel, score[y - 1][x - 1] + m]
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
    while i > -1 and j > -1:
        if backtrack[i][j] == "↓":
            istring = [vv[i]] + istring
            jstring = ["-"] + jstring
            i -= 1
        elif backtrack[i][j] == "→":
            istring = ["-"] + istring
            jstring = [ww[j]] + jstring
            j -= 1
        elif backtrack[i][j] == "↘":
            istring = [vv[i]] + istring
            jstring = [ww[j]] + jstring
            i -= 1
            j -= 1
        else:
            raise "error A"

    iout = "".join(istring)
    jout = "".join(jstring)
    return iout, jout


def match_score(v, w, indel, mismatch, match):
    """
    score 2 strings per matrix
    """
    sco = 0
    for i, _ in enumerate(v):
        if v[i] == "-" or w[i] == "-":
            sco += indel
        elif v[i] != w[i]:
            sco += mismatch
        elif v[i] == w[i]:
            sco += match
    return sco


if __name__ == "__main__":

    with open("dataset_248_7 (1).txt") as file:
        dataset = file.read().splitlines()

    v = dataset[0]
    w = dataset[1]

    # v = "PAWHEAE"
    # w = "HEAGAWGHEE"

    v = "GATACAGCACACTAGTACTACTTGAC"
    w = "CTA-TAGT-CTTAACGATATACGAC"

    indel = -2
    mismatch = 0
    match = 1
    node_scores, path_matrix = path_from_pair(v, w, indel, mismatch, match)

    print("scores size", node_scores.size)
    print("scores shape", node_scores.shape)

    print("path_matrix size", path_matrix.size)
    print("path_matrix shape", path_matrix.shape)

    ## get first occurence of highest score in the last col
    y = len(v)
    i = y - 1

    c = node_scores[-1, :][::-1]
    x = len(c) - np.argmax(c) - 1
    j = x - 1

    ## string starts on left most col and ends on bottom most row
    print("end", i, j, node_scores[y][x])

    istring, jstring = back_path(path_matrix, v, w, i, j)
    print("score quiz4")
    print(match_score(istring, jstring, indel, mismatch, match))
    print(istring)
    print(jstring)

    v = "CTAGTACTACTTGAC"
    w = "CTA-TAGT-CTTAAC"
    print("quiz4 ", match_score(v, w, indel, mismatch, match))

    # quiz 1
    v = "TCGAC--ATT"
    w = "CC---GAA-T"
    indel = -2
    mismatch = -1
    match = 1
    print("quiz1", match_score(v, w, indel, mismatch, match))

    # quiz 3
