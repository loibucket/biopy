import numpy as np


def manhattan_tourist(n, m, downs, rights):
    score = np.zeros((n + 1, m + 1), dtype=int)

    for i in range(1, n + 1):
        score[i][0] = score[i - 1][0] + downs[i - 1][0]

    for j in range(1, m + 1):
        score[0][j] = score[0][j - 1] + rights[0][j - 1]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            score[i][j] = max(score[i - 1][j] + downs[i - 1][j], score[i][j - 1] + rights[i][j - 1])

    return score[-1][-1]


if __name__ == "__main__":

    file = "dataset_261_10 (1).txt"
    with open(file) as f:
        dataset = f.read().splitlines()

    n, m = [int(value) for value in dataset[0].split(" ")]

    downs = []
    for i in range(n):
        downs.append([int(value) for value in dataset[i + 1].split(" ")])
    downs = np.array(downs)

    rights = []
    for j in range(n + 1):
        rights.append([int(value) for value in dataset[j + 1 + n + 1].split(" ")])
    rights = np.array(rights)

    print("n", n, "m", m)
    print("downs\n", downs)
    print("rights\n", rights)

    out = manhattan_tourist(n, m, downs, rights)
    print(out)
