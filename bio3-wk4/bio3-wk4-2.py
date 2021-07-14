def num_breakpoints(inp):
    """
    find number of breakpoints in a seq
    """
    perm = [0] + inp.copy()

    breaks = 0

    if perm[1] != 1:
        breaks += 1

    if perm[len(inp)] != len(inp):
        breaks += 1

    for i in range(2, len(inp) + 1):

        if perm[i] - perm[i - 1] != 1:
            breaks += 1

    return breaks


if __name__ == "__main__":

    inp = "+6 -12 -9 +17 +18 -4 +5 -3 +11 +19 +20 +10 +8 +15 -14 -13 +2 +7 -16 -1"

    inp = [int(i) for i in inp.split()]

    out = num_breakpoints(inp)

    print(out)
