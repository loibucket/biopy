"""
alignment between sequences 
"""

import numpy as np


def score_wfile(file):
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


def backtrack_wmatrix(v, w, indel, score_matrix):
    """
    given strings v and w, construct a backtrack matrix
    """
    # use y x coords for score (nodes), use i j coords for backtrack (paths)
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

    return score, backtrack


def backtrack_wconstants(v, w, indel, mismatch, match):
    """
    given strings v and w, construct a backtrack matrix
    """
    ## use y x coords for score (nodes), use i j coords for backtrack (paths)
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

    return score, backtrack


def backtrack_localfit(v, w, indel, mismatch, match):
    """
    given strings v and w, construct a path matrix
    """
    ## use y x coords for score (nodes), use i j coords for backtrack (paths)
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
    directions = {0: "x", 1: "↓", 2: "→", 3: "↘"}

    for i in range(len(v)):
        for j in range(len(w)):
            m = match if v[i] == w[j] else mismatch
            y, x = i + 1, j + 1
            score_list = [0, score[y - 1][x] + indel, score[y][x - 1] + indel, score[y - 1][x - 1] + m]
            high_score = max(score_list)
            score[y][x] = high_score
            backtrack[i][j] = directions[score_list.index(high_score)]

    return score, backtrack


def align_pair(backtrack, v, w, i, j, align_all=True):
    """
    output path generated alignment created by backtrack
    """
    vv = list(v)
    ww = list(w)
    istring = []
    jstring = []

    path = np.full((len(v), len(w)), " ")

    while i > -1 and j > -1:
        path[i, j] = "x"
        b = backtrack[i][j]
        if b == "↓":
            istring = [vv[i]] + istring
            jstring = ["-"] + jstring
            i -= 1
        elif b == "→":
            istring = ["-"] + istring
            jstring = [ww[j]] + jstring
            j -= 1
        elif b == "↘":
            istring = [vv[i]] + istring
            jstring = [ww[j]] + jstring
            i -= 1
            j -= 1
        else:
            break

    if align_all:
        while i > -1:
            istring = [vv[i]] + istring
            jstring = ["-"] + jstring
            i -= 1

        while j > -1:
            istring = ["-"] + istring
            jstring = [ww[j]] + jstring
            j -= 1

    iout = "".join(istring)
    jout = "".join(jstring)
    return iout, jout, path


def match_score_wconstants(v, w, indel, mismatch, match):
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


def match_score_wmatrix(v, w, indel, score_matrix):
    """
    score 2 strings per matrix
    """
    sco = 0
    for i, _ in enumerate(v):
        if v[i] == "-" or w[i] == "-":
            sco += indel
        else:
            sco += score_matrix[":".join(sorted([v[i], w[i]]))]
    return sco


if __name__ == "__main__":
    pass
