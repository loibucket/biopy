import numpy as np
import copy


def dist_btw_leaves(n, adj_dict, mx_node):
    """
    populate the distance matrix from given adj_list graph
    include only leaf nodes in the output
    nodes < n are leaf nodes
    """
    z = mx_node + 1
    mat = np.zeros((z, z))

    for k, v in adj_dict.items():
        mat[k[0], k[1]] = v
        mat[k[1], k[0]] = v

    def recur(origin, cursor, paths, w):
        """
        recursion helper
        given origin node, current node as cursor, accumlated weight, open paths
        record current location into matrix
        update open paths, move cursor to next valid node
        """

        mat[cursor, origin] = w
        mat[origin, cursor] = w

        quals = [t for t in paths.keys() if (t[0] == cursor or t[1] == cursor)]

        if not quals:
            return

        new_paths = copy.deepcopy(paths)
        for q in quals:
            new_paths.pop(q)

        for q in quals:

            weight = paths[q]
            new_w = w + weight

            if q[0] == cursor:
                x = q[1]
            elif q[1] == cursor:
                x = q[0]

            recur(origin, x, new_paths, new_w)

    for i in range(z):
        recur(i, i, adj_dict, 0)

    return mat[:n, :n]


if __name__ == "__main__":

    # read D matrix
    with open("dataset_10329_11t.txt") as f:
        data = f.read().splitlines()

    # sample file content
    """
    0 3 4 3
    3 0 4 5
    4 4 0 2
    3 5 2 0
    """

    mat = []
    for line in data:
        mat.append([int(i) for i in line.split()])

    mat = np.array(mat)

    print(mat)

    # read T graph and get distance matrix
    with open("dataset_10328_12t.txt") as f:
        data = f.read().splitlines()

    # sample file content
    """
    4
    0->4:3
    1->4:4
    4->5:5
    5->2:1
    5->3:2
    """

    n = int(data[0])

    mx = 0
    adj_dict = {}
    for line in data[1:]:
        a, b, c = [int(i) for i in line.replace("->", ":").split(":")]
        adj_dict[tuple(sorted((a, b)))] = c
        mx = max(mx, a, b)

    # print(mx, n, adj_dict)

    tmat = dist_btw_leaves(n, adj_dict, mx)
    print(tmat)

    # compute least squares
    diff = mat - tmat
    print(diff)

    powe = np.power(diff, 2)
    print(powe)

    print(sum(sum(powe)) / 2)  # divide by 2 to get half triangle of matrix
