from collections import defaultdict


def defdict():
    return []


def reverse_complement(seq):
    """
    reverse complement of a sequence, which is the other strand the seq binds to
    """
    dct = {"A": "T", "T": "A", "C": "G", "G": "C"}
    mer = ""
    for char in seq:
        mer = dct[char] + mer
    return mer


def shared_kmers(k, sta, stb):
    """
    get all shared k-mers between sta and stb
    """

    b_dct = defaultdict(defdict)
    for i, _ in enumerate(stb[: -k + 1]):
        b_dct[stb[i : i + k]].append(i)

    matches = []
    for i, _ in enumerate(sta[: -k + 1]):
        match = sta[i : i + k]
        rev_match = reverse_complement(match)

        for compare in (match, rev_match):
            if compare in b_dct.keys():
                for v in b_dct[compare]:
                    matches.append((i, v))

    return matches


if __name__ == "__main__":

    k = 3
    sta = "AAACTCATC"
    stb = "TTTCAAATC"

    with open("dataset_289_5 (1).txt") as f:
        data = f.read().splitlines()
        k = int(data[0])
        sta = data[1]
        stb = data[2]

    k = 30
    with open("E_coli.txt") as f:
        data = f.read().splitlines()
        sta = data[0]
    with open("Salmonella_enterica.txt") as f:
        data = f.read().splitlines()
        stb = data[0]

    k = 2
    sta = "AAACTCATC"
    stb = "TTTCAAATC"

    k = 3
    sta = "TGCCCCGGTGGTGAG"
    stb = "AAGGTCGCACCTCGT"

    out = shared_kmers(k, sta, stb)
    print(out)
    print(len(set(out)))

    with open("dataset_289_5_out.txt", "w") as f:
        for o in out:
            f.write(str(o) + "\n")
