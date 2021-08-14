import numpy as np
import networkx as nx


def upgma(D, n):
    pass


if __name__ == "__main__":

    with open("dataset_10332_8s.txt") as f:
        data = f.read().splitlines()

        n = data[0]
        d = data[1:]

    mat = []
    for line in d:
        mat.append([int(i) for i in line.split()])

    mat = np.array(mat)

    print(n)
    print(mat)
