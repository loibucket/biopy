from collections import defaultdict


def def_value():
    return 0


def FreqTable(seq, k):
    dct = defaultdict(def_value)
    for i in range(0, len(seq)-k+1):
        dct[seq[i:int(i+k)]] += 1
    return dct


def FindClumps(Text, k, L, t):
    Patterns = set([])
    n = len(Text)
    for i in range(0, n-L+1):
        Window = Text[i:i+L]
        freqMap = FreqTable(Window, k)
        for s in freqMap:
            if freqMap[s] >= t:
                Patterns.add(s)
    return " ".join(Patterns)


if __name__ == "__main__":

    with open("E_coli.txt", "r") as f:
        data = f.read()

    tup = (
        ("AAAACGTCGAAAAA", 2, 4, 2),
        (data, 9, 500, 3),
    )

    def test(tup):
        for t in tup:
            print(FindClumps(*t))

    test(tup)
