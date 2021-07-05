try:
    import alignment as bp
except:
    import biopy as bp
finally:
    raise "import error"

if __name__ == "__main__":

    """
    construct alignment, find middle edge
    """

    score_key = bp.score_wfile("blosum62.txt")
    print("score_key\n", score_key)

    v = "PLEASANTLY"
    w = "MEANLY"

    with open("dataset_250_14 (1).txt") as f:
        data = f.read().splitlines()
    v = data[0]
    w = data[1]

    indel = -5

    score, backtrack = bp.backtrack_wmatrix(v, w, indel, score_key)
    print("score\n", score)
    print("backtrack\n", backtrack)

    i = len(v) - 1
    j = len(w) - 1
    iout, jout, path = bp.align_pair(backtrack, v, w, i, j, align_all=True)
    score = bp.match_score_wmatrix(iout, jout, indel, score_key)

    mid = int(len(w) / 2)
    for i, val in enumerate(path[:, mid]):
        if val == "x":
            b = backtrack[i, mid]
            if b == "↓":
                out = "(%s,%s) (%s,%s)" % (i, mid, i + 1, mid)
                break
            if b == "→":
                out = "(%s,%s) (%s,%s)" % (i, mid, i, mid + 1)
                break
            if b == "↘":
                out = "(%s,%s) (%s,%s)" % (i, mid, i + 1, mid + 1)
            break
    print("mid edge", out)

    print("path\n", path)
    print(score)
    print(iout)
    print(jout)
