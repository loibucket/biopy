import numpy as np

np.set_printoptions(precision=3)


def backtrack_three(v, w, u):
    """
    given strings v w u, construct a backtrack matrix
    """
    ## use y x z coords for score (nodes), use i j k coords for backtrack (paths)
    score = np.zeros((len(v) + 1, len(w) + 1, len(u) + 1), dtype=int)

    backtrack = np.full((len(v), len(w), len(u)), ".")
    directions = ["1", "2", "3", "a", "b", "c", "d"]

    for i in range(len(v)):
        for j in range(len(w)):
            for k in range(len(u)):
                m = 1 if v[i] == w[j] == u[k] else 0

                y, x, z = i + 1, j + 1, k + 1
                s1 = score[y - 1, x, z]
                s2 = score[y, x - 1, z]
                s3 = score[y, x, z - 1]

                sa = score[y - 1, x, z - 1]
                sb = score[y, x - 1, z - 1]
                sc = score[y - 1, x - 1, z]
                sd = score[y - 1, x - 1, z - 1] + m

                score_list = [s1, s2, s3, sa, sb, sc, sd]

                high_score = max(score_list)
                score[y, x, z] = high_score

                backtrack[i, j, k] = directions[score_list.index(high_score)]

    return score, backtrack


def align_three(backtrack, v, w, u, i, j, k):
    """
    output path generated alignment created by backtrack
    """
    vv = list(v)
    ww = list(w)
    uu = list(u)
    istring = []
    jstring = []
    kstring = []

    path = np.full((len(v), len(w), len(u)), " ", dtype="<U100")

    p = 0
    while i > -1 and j > -1 and k > -1:
        p += 1
        path[i, j, k] = p
        bk = backtrack[i, j, k]
        if bk == "1":
            istring = [vv[i]] + istring
            jstring = ["-"] + jstring
            kstring = ["-"] + kstring
            i -= 1
            continue
        if bk == "2":
            istring = ["-"] + istring
            jstring = [ww[j]] + jstring
            kstring = ["-"] + kstring
            j -= 1
            continue
        if bk == "3":
            istring = ["-"] + istring
            jstring = ["-"] + jstring
            kstring = [uu[k]] + kstring
            k -= 1
            continue
        if bk == "a":
            istring = [vv[i]] + istring
            jstring = ["-"] + jstring
            kstring = [uu[k]] + kstring
            i -= 1
            k -= 1
            continue
        if bk == "b":
            istring = ["-"] + istring
            jstring = [ww[j]] + jstring
            kstring = [uu[k]] + kstring
            j -= 1
            k -= 1
            continue
        if bk == "c":
            istring = [vv[i]] + istring
            jstring = [ww[j]] + jstring
            kstring = ["-"] + kstring
            i -= 1
            j -= 1
            continue
        if bk == "d":
            istring = [vv[i]] + istring
            jstring = [ww[j]] + jstring
            kstring = [uu[k]] + kstring
            i -= 1
            j -= 1
            k -= 1
            continue

        raise "error A"

    while i > -1 or j > -1 or k > -1:

        if i > -1:
            istring = [vv[i]] + istring
        else:
            istring = ["-"] + istring

        if j > -1:
            jstring = [ww[j]] + jstring
        else:
            jstring = ["-"] + jstring

        if k > -1:
            kstring = [uu[k]] + kstring
        else:
            kstring = ["-"] + kstring

        i -= 1
        j -= 1
        k -= 1

    iout = "".join(istring)
    jout = "".join(jstring)
    kout = "".join(kstring)

    return iout, jout, kout, path


if __name__ == "__main__":

    v = "ATATCCG"
    w = "TCCGA"
    u = "ATGTACTG"

    v = "AACCAGAC"
    w = "CATGTTAC"
    u = "ATACGTAAGG"

    v = "GGCCGTAAG"
    w = "GCGGTCCGTG"
    u = "GTACCTCTA"

    v = "TCTAGCGAAC"
    w = "ATTACCGATC"
    u = "TTCACTGACG"

    score, backtrack = backtrack_three(v, w, u)

    print("score\n", score)
    print("backtrack\n", backtrack)

    i = len(v) - 1
    j = len(w) - 1
    k = len(u) - 1

    iout, jout, kout, path = align_three(backtrack, v, w, u, i, j, k)

    print(score[-1, -1, -1])
    print(iout)
    print(jout)
    print(kout)

    print(path)
