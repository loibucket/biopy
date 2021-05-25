def PatternMatch(pat, seq):
    lst = []
    for i in range(0, len(seq)-len(pat)+1):
        if seq[i:i+len(pat)] == pat:
            lst.append(str(i))
    return " ".join(lst)


if __name__ == "__main__":

    with open("Vibrio_cholerae.txt", "r") as f:
        data = f.read()

    # dct={
    #     "CTTGATCAT":data
    # }
    dct = {
        "ATA": "GACGATATACGACGATA"
    }

    def test(dct):
        for pat in dct:
            print(pat, dct[pat], PatternMatch(pat, dct[pat]))

    test(dct)
