"""
1.3 The Changing Faces of Sequence Alignment
Levenshtein introduced edit distance but did not describe an algorithm for computing it, which we leave to you.
Edit Distance Problem: Find the edit distance between two strings.

Input: Two strings.
Output: The edit distance between these strings.
Code Challenge: Solve the Edit Distance Problem.
"""

import numpy as np
from numpy import unravel_index


def path_from_pair(v, w, indel, mismatch, match):
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
    print(iout, "\n", jout)
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

    with open("dataset_248_3.txt") as file:
        dataset = file.read().splitlines()

    v = dataset[0]
    w = dataset[1]

    # v = "PLEASANTLY"
    # w = "MEANLY"

    indel = -1
    mismatch = -1
    match = 0
    node_scores, path_matrix = path_from_pair(v, w, indel, mismatch, match)
    i = len(v) - 1
    j = len(w) - 1
    istring, jstring = back_path(path_matrix, v, w, i, j)
    print("score", match_score(istring, jstring, indel, mismatch, match))
