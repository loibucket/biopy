import numpy as np
from numpy import unravel_index

"""
Code Challenge: Solve the Local Alignment Problem.

Input: Two protein strings written in the single-letter amino acid alphabet.
Output: The maximum score of a local alignment of the strings, followed by a local alignment of these strings achieving the maximum score. Use the PAM250 scoring matrix for matches and mismatches as well as the indel penalty σ = 5.
"""


def score_from_file(f):
    """
    build a map of pair scores from file
    """
    with open(f) as file:
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
    directions = {0: "x", 1: "↓", 2: "→", 3: "↘"}

    for i in range(len(v)):
        for j in range(len(w)):
            pair = [v[i], w[j]]
            pair = ":".join(sorted(pair))
            y, x = i + 1, j + 1
            score_list = [0, score[y - 1][x] + indel, score[y][x - 1] + indel, score[y - 1][x - 1] + score_matrix[pair]]
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
        if backtrack[i][j] == "x":
            return ["".join(istring), "".join(jstring)]
        elif backtrack[i][j] == "↓":
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

    raise "error B"

    print("v", istring)
    print("w", jstring)
    return ["".join(istring), "".join(jstring)]


def match_score(v, w, indel, score_matrix):
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

    score_matrix = score_from_file("pam250.txt")
    print("score_matrix\n", score_matrix)

    with open("dataset_247_10 (5).txt") as file:
        dataset = file.read().splitlines()

    v = dataset[0]
    w = dataset[1]

    # v = "MEANLY"
    # w = "PENALTY"

    # v = "ATGVWYYYYC"
    # w = "GYYCFFF"

    # v = "AAAAAASSSSSSSVVVVVVVVTTTTTTTLLLLLL"
    # w = "SSSSLLLLLTTTTTTTWWWWWWWWWWWPPPPPPPPPP"

    # v = "QTVHQIWMKRLASFFFSMMMRRLLQQSSSTTTFQQDWLLLLLSSSCCSPQPQPQTYTYTYTFFRRRSSMMMLNNNDNDKVWSKLLWPPPPQRMS"
    # w = "TQDFFSMLRRAAQFFMMRLCCDPPPATATATFPFPMMMDSNSSSDNSQRRQRQRQTFTDTSTCCQVVMNFRMNFRVDFPLLK"

    indel = -5
    node_scores, path_matrix = path_from_pair(v, w, indel, score_matrix)
    print("size", node_scores.size)
    print("shape", node_scores.shape)
    print("max score", np.amax(node_scores))
    maxindex = node_scores.argmax()
    y, x = unravel_index(node_scores.argmax(), node_scores.shape)
    print("index", y, x, node_scores[y][x])

    i = y - 1
    j = x - 1
    istring, jstring = back_path(path_matrix, v, w, i, j)

    print(node_scores[y][x])
    print(istring)
    print(jstring)

    print("score check", match_score(istring, jstring, indel, score_matrix))


## hilite.me converts your code snippets into pretty-printed HTML format, easily embeddable into blog posts, emails and websites.
