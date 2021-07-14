def greedy_sorting(p):
    """
    sorting by reversal
    """
    perm = [0] + p.copy()
    seq = []
    steps = 0

    i = 1
    while i < len(perm):

        if perm[i] == i:
            i += 1
            continue

        if perm[i] == -i:
            perm[i] = i
            print(perm[1:])
            seq.append(clean_print(perm[1:]))
            steps += 1
            continue

        if perm[i] != i:
            if i in perm:
                found = perm.index(i)
            elif -i in perm:
                found = perm.index(-i)
            else:
                raise Exception("error A")

            perm = reverse_perm(perm, i, found)
            print(perm[1:])
            seq.append(clean_print(perm[1:]))
            steps += 1
            continue

        raise Exception("error B")

    print("steps", steps)

    return seq


def reverse_perm(p, start, end):
    """
    do a reversal
    """
    perm = p.copy()

    a = perm[:start]
    b = [-i for i in perm[start : end + 1][::-1]]
    c = perm[end + 1 :]

    return a + b + c


def clean_print(p):
    """
    clean up for output
    """
    st = ""
    for c in p:
        if c > 0:
            st += " +" + str(c)
        else:
            st += " " + str(c)

    if st[0] == " ":
        return st[1:]
    return st


if __name__ == "__main__":

    # inp = "-3 +4 +1 +5 -2"
    # inp = "+112 +93 -70 -122 -60 +119 +26 -98 -21 +126 -8 -42 -62 -46 +117 +49 +40 +35 -18 -86 -50 -91 +139 +118 +63 -64 -79 -110 +44 -123 -39 +87 +55 +68 +74 +138 +31 -90 +71 +37 -134 +94 -6 +3 -34 -7 +146 -128 -65 +12 -4 -25 -114 +145 +107 +80 -72 +127 +95 +75 +53 +103 -106 -147 +100 -9 -28 +88 -116 +77 +36 -10 -19 -81 -17 -131 -57 -29 -148 +83 -85 +89 -67 +104 -13 +66 -130 -43 +27 -1 -2 -54 -59 -109 +111 -140 -45 -73 -132 -135 -137 +121 +69 +11 -97 -142 -115 -124 -16 -56 +99 +92 -58 +61 +84 +78 +105 +48 +136 +149 +76 +144 +129 -30 +96 -38 +143 -33 +24 +14 -23 -5 -125 -15 +51 +52 -108 +47 -82 -113 +101 -32 +102 -20 -22 -120 +133 +141 -41"

    # with open("dataset_286_4.txt") as f:
    #     inp = f.read().splitlines()[0]

    inp = "+20 +7 +10 +9 +11 +13 +18 -8 -6 -14 +2 -4 -16 +15 +1 +17 +12 -5 +3 -19"

    inp = [int(i) for i in inp.split()]

    out = greedy_sorting(inp)

    with open("dataset_286_4_out.txt", "w") as f:
        for l in out:
            f.write(l + "\n")
        # manually delete last blank line before submitting
