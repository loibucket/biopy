from collections import defaultdict
import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


def defvalue():
    return 0


def spectrum_score(peptide, spectrum):
    """
    find the score of a spectrum against a given peptide
    """
    actual = bp.cyclo_aa_spectrum(peptide)
    actual_map = defaultdict(defvalue)
    for s in actual:
        actual_map[s] += 1

    score = 0
    for m in spectrum:
        if actual_map[m] > 0:
            actual_map[m] -= 1
            score += 1

    return score


if __name__ == "__main__":

    pep = "NQEL"
    spec = "0 99 113 114 128 227 257 299 355 356 370 371 484"
    spec = [int(s) for s in spec.split(" ")]

    out = spectrum_score(pep, spec)
    print(out)

    with open("dataset_102_3.txt") as file:
        pep, spec = file.read().splitlines()
        spec = [int(s) for s in spec.split(" ")]

    out = spectrum_score(pep, spec)
    print(out)
