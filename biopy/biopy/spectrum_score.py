import biopy as bp
from collections import defaultdict


def defvalue():
    return 0


def spectrum_aa_score(peptide, input_spectrum, linear=False):
    """
    find the score of a spectrum against a given peptide, as a aa sequence
    """
    if not input_spectrum:
        return 0

    spectrum = input_spectrum.copy()

    if linear:
        test = bp.linear_aa_spectrum(peptide)
    else:
        test = bp.cyclo_aa_spectrum(peptide)

    score = 0
    t = test.pop()
    s = spectrum.pop()

    while s:
        if t == s:
            score += 1
            t = test.pop() if test else None
            s = spectrum.pop() if spectrum else None
        elif t < s:
            s = spectrum.pop() if spectrum else None
        elif t > s:
            t = test.pop() if test else None
            
    return score


def spectrum_mass_score(peptide, input_spectrum, linear=False):
    """
    find the score of a spectrum against a given peptide, as a mass sequence
    """
    if not input_spectrum:
        return 0

    spectrum = input_spectrum.copy()

    if linear:
        test = bp.linear_mass_spectrum(peptide)
    else:
        test = bp.cyclo_mass_spectrum(peptide)

    score = 0
    t = test.pop()
    s = spectrum.pop()

    while s:
        if t == s:
            score += 1
            t = test.pop() if test else None
            s = spectrum.pop() if spectrum else None
        elif t < s:
            s = spectrum.pop() if spectrum else None
        elif t > s:
            t = test.pop() if test else None
            
    return score


if __name__ == "__main__":

    pep = "NQEL"
    spec = "0 99 113 114 128 227 257 299 355 356 370 371 484"
    spec = [int(s) for s in spec.split(" ")]

    out = spectrum_aa_score(pep, spec)
    print(out)

    # with open("dataset_102_3.txt") as file:
    #     pep, spec = file.read().splitlines()
    #     spec = [int(s) for s in spec.split(" ")]

    # out = spectrum_score(pep, spec)
    # print(out)

    pep=[1,1]
    spec=[1,2,3,4]
    out = spectrum_mass_score(pep, spec)
    print(out)