import numpy as np
from collections import defaultdict


def def_list():
    return []


def def_zero():
    return 0


def lcs_backtrack(v, w):
    """
    given strings v and w, construct a path matrix
    """
    score = np.zeros((len(v) + 1, len(w) + 1), dtype=int)
    backtrack = np.full((len(v), len(w)), ".")

    for i in range(len(v)):
        for j in range(len(w)):
            match = 0
            if v[i] == w[j]:
                match = 1
            score[i][j] = max(score[i - 1][j], score[i][j - 1], score[i - 1][j - 1] + match)
            if score[i][j] == score[i - 1][j]:
                backtrack[i][j] = "↓"
            elif score[i][j] == score[i][j - 1]:
                backtrack[i][j] = "→"
            else:
                backtrack[i][j] = "↘"

    print(score)
    print(backtrack)
    return backtrack


def output_lcs(backtrack, v, i, j):
    """
    longest common string
    """
    lcs = []
    while True:
        if i == -1 or j == -1:
            break
        if backtrack[i][j] == "↓":
            i -= 1
        elif backtrack[i][j] == "→":
            j -= 1
        elif backtrack[i][j] == "↘":
            lcs = [v[i]] + lcs
            i -= 1
            j -= 1
    return "".join(lcs)


def dag_scores(start, end, edges):
    """
    build a dict of scores from given dag
    """

    scores = defaultdict(def_zero)
    cursors = [start]
    scores[start] = 0

    while True:

        new_cursors = []
        for cur in cursors:
            next_steps = edges[str(cur)]
            for nex in next_steps:
                node, weight = nex.split(":")
                weight = int(weight)
                scores[node] = max(scores[node], scores[cur] + weight)
                new_cursors.append(node)
        if not new_cursors:
            break
        else:
            cursors = new_cursors

    print("scores", scores)
    return scores


def back_dag(start, end, edges, scores):
    """
    build longest path from given dag and scores
    """

    # build backtrack dictinoary
    backtrack = defaultdict(def_list)
    for key, value in edges.items():
        for nex in value:
            org = str(key)
            vals = nex.split(":")
            dest = str(vals[0])
            weight = str(vals[1])
            backtrack[dest].append(org + ":" + weight)

    path = [end]
    cursor = end
    while True:

        choices = backtrack[str(cursor)]
        for cho in choices:
            node, weight = cho.split(":")
            weight = int(weight)
            if scores[node] + weight == scores[cursor]:
                path = [node] + path
                cursor = node

        if cursor == start:
            break

    path = [str(pa) for pa in path]

    return "->".join(path)


if __name__ == "__main__":

    with open("dataset_quiz.txt") as f:
        dataset = [line.replace(" ", "") for line in f.read().splitlines() if line]

    start = dataset[0]
    end = dataset[1]
    edges = defaultdict(def_list)

    for i in range(2, len(dataset)):
        dct = dataset[i].split("->")
        edges[dct[0]].append(dct[1])

    print(start, end, edges)

    scores = dag_scores(start, end, edges)
    print(scores)
    print(scores[end])
    out = back_dag(start, end, edges, scores)
    print(out)


if __name__ == "__main__x":
    v = "GCGATC"
    w = "CTGACG"

    backtrack = lcs_backtrack(v, w)
    out = output_lcs(backtrack, v, len(v) - 1, len(w) - 1)
    print(out)

    with open("dataset_245_5 (7).txt") as f:
        dataset = f.read().splitlines()
        v = dataset[0]
        w = dataset[1]

    backtrack = lcs_backtrack(v, w)
    out = output_lcs(backtrack, v, len(v) - 1, len(w) - 1)
    print(out)
