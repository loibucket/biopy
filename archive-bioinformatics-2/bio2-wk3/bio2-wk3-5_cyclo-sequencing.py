import copy
import itertools
import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


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


def expand_peptides(peptides, masses=mass_map()):
    """
    a new collection containing all possible extensions of peptides in Peptides by a single amino acid mass
    """
    new_peptides = []
    for p in peptides:
        for a_mass in masses.keys():
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

    ## test linear mass spectrum

    # peptide = [1, 2, 3, 4]
    # print(bp.linear_mass_spectrum(peptide))

    # peptide = [114, 128, 129, 113]
    # print(bp.linear_mass_spectrum(peptide))

    # amino_acid_mass = {
    #     "G": 57,
    #     "A": 71,
    #     "S": 87,
    #     "P": 97,
    #     "V": 99,
    #     "T": 101,
    #     "C": 103,
    #     "I": 113,
    #     "L": 113,
    #     "N": 114,
    #     "D": 115,
    #     "K": 128,
    #     "Q": 128,
    #     "E": 129,
    #     "M": 131,
    #     "H": 137,
    #     "F": 147,
    #     "R": 156,
    #     "Y": 163,
    #     "W": 186,
    # }

    # string = "MPYENCCCWMFNIRKGQPDFFRKGAVPYVVPMNCIRWS"
    # peptide = []
    # for s in string:
    #     peptide.append(amino_acid_mass[s])
    # print(peptide)
    # out = bp.linear_mass_spectrum(peptide)
    # out = [str(o) for o in out]
    # output = "0 57 57 71 87 97 97 97 97 99 99 99 103 103 103 103 113 113 114 114 114 115 128 128 128 128 129 131 131 131 147 147 147 156 156 156 163 163 170 185 185 185 186 186 196 196 198 206 206 212 216 217 217 225 227 227 228 228 243 245 256 260 260 261 262 262 267 269 269 273 278 282 284 284 289 292 294 295 303 309 313 317 320 324 327 330 340 341 341 342 342 346 348 355 359 359 359 361 372 374 383 389 391 392 392 397 397 406 409 410 412 420 423 426 429 430 431 441 445 449 450 452 454 455 458 458 458 461 464 469 486 487 487 488 495 503 505 506 509 511 511 520 523 525 529 530 540 542 544 544 552 555 557 558 558 559 565 566 567 568 578 578 582 586 589 606 608 609 612 615 617 626 628 634 634 635 643 645 654 657 658 658 661 662 670 672 672 679 681 681 685 686 691 691 693 696 703 706 709 714 714 715 715 725 737 738 740 750 755 756 759 771 773 782 784 785 789 790 790 793 794 794 800 803 805 806 812 813 813 819 821 828 840 843 846 847 847 847 856 869 870 887 887 890 897 899 900 901 902 903 908 910 912 913 918 918 918 919 920 940 941 943 950 969 970 974 975 975 975 975 975 987 998 999 1000 1001 1002 1016 1016 1017 1017 1017 1027 1032 1032 1032 1041 1046 1053 1055 1055 1065 1066 1071 1073 1075 1078 1086 1088 1098 1103 1103 1114 1114 1115 1116 1129 1129 1130 1130 1131 1135 1145 1155 1156 1160 1160 1164 1172 1179 1180 1181 1185 1186 1186 1197 1202 1202 1202 1213 1231 1238 1242 1243 1243 1244 1257 1258 1259 1260 1261 1263 1263 1270 1271 1276 1277 1279 1284 1293 1299 1311 1316 1330 1333 1341 1342 1344 1348 1349 1358 1358 1360 1360 1366 1371 1372 1372 1376 1378 1387 1390 1398 1399 1399 1405 1406 1407 1414 1427 1429 1445 1455 1457 1458 1462 1463 1469 1475 1475 1475 1480 1486 1486 1491 1500 1503 1504 1505 1519 1521 1527 1527 1527 1528 1543 1544 1561 1561 1562 1566 1572 1578 1583 1583 1584 1585 1590 1599 1603 1605 1606 1614 1615 1622 1633 1634 1636 1659 1660 1666 1672 1674 1680 1681 1683 1689 1690 1690 1696 1700 1703 1708 1712 1713 1713 1720 1725 1746 1747 1757 1761 1764 1769 1787 1788 1790 1795 1800 1809 1810 1817 1821 1821 1822 1823 1828 1830 1831 1844 1845 1859 1860 1869 1872 1875 1885 1888 1892 1918 1920 1924 1925 1936 1942 1944 1945 1950 1956 1957 1958 1972 1972 1973 1975 1975 1977 1991 2002 2007 2016 2016 2028 2033 2041 2048 2053 2057 2069 2071 2072 2078 2087 2088 2089 2092 2103 2103 2105 2110 2120 2130 2131 2154 2156 2161 2163 2171 2172 2177 2181 2184 2189 2200 2213 2218 2218 2219 2233 2234 2245 2250 2251 2259 2268 2274 2278 2280 2284 2285 2286 2315 2316 2317 2318 2331 2346 2350 2365 2373 2374 2374 2375 2377 2381 2383 2387 2389 2399 2399 2415 2430 2437 2449 2462 2462 2478 2480 2486 2501 2502 2502 2502 2502 2503 2513 2536 2537 2540 2546 2546 2559 2560 2583 2590 2600 2609 2615 2616 2630 2634 2635 2639 2643 2647 2658 2660 2665 2677 2688 2697 2722 2729 2729 2732 2738 2742 2746 2762 2763 2765 2771 2775 2791 2793 2819 2826 2835 2841 2844 2845 2860 2863 2876 2885 2890 2892 2893 2894 2931 2938 2944 2950 2957 2959 2966 2977 2989 2989 2989 3007 3021 3032 3041 3044 3058 3069 3071 3080 3080 3086 3088 3120 3152 3155 3158 3163 3172 3183 3183 3187 3193 3217 3218 3249 3251 3284 3286 3286 3286 3296 3305 3348 3349 3349 3350 3380 3389 3399 3400 3415 3436 3447 3447 3452 3479 3502 3503 3529 3535 3544 3555 3578 3578 3616 3622 3632 3638 3658 3675 3675 3692 3725 3741 3745 3772 3789 3795 3806 3828 3844 3892 3901 3908 3920 3931 3958 4005 4023 4045 4064 4087 4136 4161 4174 4250 4292 4337 4347 4434 4478 4565"
    # print(" ".join(out) == output)
