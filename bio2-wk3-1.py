

def rna_to_aa(seq, table):
    aa = []
    length = len(seq)
    for i in range(0, length, 3):
        triplet = ("").join((seq[i], seq[i+1], seq[i+2]))
        aa.append(table[triplet])
    return ("").join(aa)


if __name__ == "__main__":
    codon_table = {}

    with open("RNA_codon_table_1.txt") as dataset:
        raw = dataset.read().splitlines()
        for row in raw:
            cols = row.split()
            if len(cols) > 1:
                codon_table[cols[0]] = cols[1]
            else:
                codon_table[cols[0]] = ""

    # print(codon_table)
    out = rna_to_aa("AUGGCCAUGGCGCCCAGAACUGAGAUCAAUAGUACCCGUAUUAACGGGUGA", codon_table)
    print(out)
    print("out ==  MAMAPRTEINSTRING", out == "MAMAPRTEINSTRING")

    with open("bio2-wk3-1data-in.txt") as dataset:
        seq = dataset.read().splitlines()[0]
        # print(seq)
        out = rna_to_aa(seq, codon_table)

    with open("out_wk3-1.txt", "w") as record:
        record.write(out)

    with open("bio2-wk3-1data-out.txt") as dataset:
        ans = dataset.read().splitlines()[0]
        print("out==ans", out == ans)

    #####

    with open("dataset_96_4.txt") as dataset:
        seq = dataset.read().splitlines()[0]
        # print(seq)
        out = rna_to_aa(seq, codon_table)
    with open("out_96_4.txt", "w") as record:
        record.write(out)
