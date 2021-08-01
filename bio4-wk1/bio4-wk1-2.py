import numpy as np
import math


def limblength(j, mat):
    """
    get the limb length of species j
    """
    minval = math.inf

    for i in range(len(mat)):
        for k in range(len(mat[i])):
            if i != k and j != k and i != j:
                minval = min(minval, (mat[i, j] + mat[j, k] - mat[i, k]) / 2.0)

    return int(minval)


if __name__ == "__main__":

    with open("dataset_10329_11quiz.txt") as f:
        data = f.read().splitlines()

    n = int(data[0])
    j = int(data[1])

    mat = []
    for line in data[2:]:
        mat.append([int(i) for i in line.split()])

    mat = np.array(mat)

    out = limblength(j, mat)
    print(out)
