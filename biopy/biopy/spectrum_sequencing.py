import biopy as bp
import copy
import itertools


def mass_map():
    # https://stepik.org/lesson/99/step/2?unit=8264
    alphabet = {
        57: "G",
        71: "A",
        87: "S",
        97: "P",
        99: "V",
        101: "T",
        103: "C",
        113: "I/L",
        114: "N",
        115: "D",
        128: "K/Q",
        129: "E",
        131: "M",
        137: "H",
        147: "F",
        156: "R",
        163: "Y",
        186: "W",
    }
    return alphabet


def expand_peptides(peptides, nonproteingenic=False, masses=mass_map()):
    """
    a new collection containing all possible extensions of peptides in Peptides by a single amino acid mass
    """
    if nonproteingenic:
        mass_list = list(range(57, 201))
    else:
        mass_list = masses.keys()

    new_peptides = []
    for p in peptides:
        for a_mass in mass_list:
            new_peptides.append(p + [a_mass])
    return new_peptides


def cyclopeptide_sequence(spectrum):
    """
    possible peptides with the given spectrum, listed as dalton masses
    https://stepik.org/lesson/100/step/6?unit=8265
    """
    spectrum.sort()
    spectrum_mass = spectrum[-1]
    candidate_peptides = [[]]
    final_peptides = []
    masses = mass_map()

    # find all peptide combinations that has same mass as spectrum parent mass
    # first loop removes non-valid masses
    loop_count = 0
    candidate_peptides = expand_peptides(candidate_peptides)
    good_peptides = []
    for pep in candidate_peptides:
        if bp.mass_sum(pep) == spectrum_mass and bp.cyclo_mass_spectrum(pep) == spectrum and pep not in final_peptides:
            final_peptides.append(pep)
            masses.pop(pep[0])
        elif not all(a in spectrum for a in pep) or bp.mass_sum(pep) > spectrum_mass:
            masses.pop(pep[0])
        else:
            good_peptides.append(pep)
    candidate_peptides = good_peptides

    print("candidates", candidate_peptides, "masses", masses)
    while candidate_peptides:
        loop_count += 1
        if loop_count > 20:
            print("loop limit exceeeded")
            break

        found = 0
        removed = 0
        kept = 0

        candidate_peptides = expand_peptides(candidate_peptides, masses)
        good_peptides = []

        print("loop", loop_count, "candidates", len(candidate_peptides))

        for pep in candidate_peptides:
            pep_spectrum = bp.cyclo_mass_spectrum(pep)
            if bp.mass_sum(pep) == spectrum_mass and bp.cyclo_mass_spectrum(pep) == spectrum and pep not in final_peptides:
                final_peptides.append(pep)
                found += 1
            elif not all(a in spectrum for a in bp.linear_mass_spectrum(pep)):
                removed += 1
            else:
                good_peptides.append(pep)
                kept += 1
        candidate_peptides = good_peptides

        print("found", found, "removed", removed, "kept", kept)

    return final_peptides


if __name__ == "__main__":
    # out = expand_peptides([[]])
    # print(out)
    # out = expand_peptides(out)
    # print(out)

    spectrum = "0 71 97 99 103 113 113 114 115 131 137 196 200 202 208 214 226 227 228 240 245 299 311 311 316 327 337 339 340 341 358 408 414 424 429 436 440 442 453 455 471 507 527 537 539 542 551 554 556 566 586 622 638 640 651 653 657 664 669 679 685 735 752 753 754 756 766 777 782 782 794 848 853 865 866 867 879 885 891 893 897 956 962 978 979 980 980 990 994 996 1022 1093"
    # spectrum = "0 113 128 186 241 299 314 427"
    spectrum = [int(s) for s in spectrum.split(" ")]
    print("spectrum", len(spectrum))
    out = cyclopeptide_sequence(spectrum)
    for ou in out:
        print("-".join([str(o) for o in ou]), end=" ")
    print("")

    spectrum = "0 71 87 97 97 103 114 115 131 156 156 163 186 200 202 212 217 218 250 253 253 270 283 289 314 317 319 356 367 368 373 381 404 406 414 416 439 452 470 470 470 482 501 503 519 537 553 567 567 570 585 606 608 626 633 634 656 657 664 682 684 705 720 723 723 737 753 771 787 789 808 820 820 820 838 851 874 876 884 886 909 917 922 923 934 971 973 976 1001 1007 1020 1037 1037 1040 1072 1073 1078 1088 1090 1104 1127 1134 1134 1159 1175 1176 1187 1193 1193 1203 1219 1290"
    # spectrum = "0 113 128 186 241 299 314 427"
    spectrum = [int(s) for s in spectrum.split(" ")]
    print("spectrum", len(spectrum))
    out = cyclopeptide_sequence(spectrum)
    for ou in out:
        print("-".join([str(o) for o in ou]), end=" ")
    print("")
