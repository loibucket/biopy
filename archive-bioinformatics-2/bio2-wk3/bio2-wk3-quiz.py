import biopy as bp

# Which of the following RNA strings could translate into the amino acid string PRTEIN? (Select all that apply.)

codon_table = bp.codon_table()

strings = "CCCAGUACCGAGAUGAAU", "CCUCGUACAGAAAUCAAC", "CCCAGGACUGAGAUCAAU", "CCUCGUACUGAUAUUAAU"

for string in strings:
    print(string)

    for i in range(0, len(string), 3):
        codon = string[i : i + 3]
        try:
            print(codon_table[codon], end="")
        except:
            print(" ", end="")

    print("")


rev_codon_table = bp.reverse_codon_table()
print(rev_codon_table)

# How many DNA strings transcribe and translate into the amino acid string CYCLIC?
string = "CYCLIC"
combos = 1
for s in string:
    print(s, len(rev_codon_table[s]))
    combos *= len(rev_codon_table[s])
print(combos)


# Which of the following cyclic peptides could have generated the theoretical spectrum 0 71 101 113 131 184 202 214 232 285 303 315 345 416? (Select all that apply.)
peptides = ["MTAL", "IAMT", "MLAT", "TMIA", "MAIT", "TAIM"]
check = "0 71 101 113 131 184 202 214 232 285 303 315 345 416"
check = [int(c) for c in check.split(" ")]
for p in peptides:
    spectrum = bp.linear_aa_spectrum(p)
    print(p, all(a in check for a in spectrum))


# Which of the following linear peptides is consistent with Spectrum = {0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333}? (Select all that apply.)
check = "0 71 99 101 103 128 129 199 200 204 227 230 231 298 303 328 330 332 333"
check = [int(c) for c in check.split(" ")]
peptides = ["CTV", "TCE", "ETC", "CET", "VAQ", "AQV"]
for p in peptides:
    spectrum = bp.linear_aa_spectrum(p)
    print(p, bp.linear_aa_spectrum(p), all(a in check for a in spectrum))

