def aa_alphabet():
    """
    all 20 amino acids in alphabet notation
    """
    abc = ['G', 'A', 'S', 'P', 'V', 'T', 'C', 'I', 'L', 'N', 'D', 'K', 'Q', 'E', 'M', 'H', 'F', 'R', 'Y', 'W']
    return abc


def aa_mass():
    """
    mass of each amino acid
    """
    amino_acid_mass = {
        'G': 57,
        'A': 71,
        'S': 87,
        'P': 97,
        'V': 99,
        'T': 101,
        'C': 103,
        'I': 113,
        'L': 113,
        'N': 114,
        'D': 115,
        'K': 128,
        'Q': 128,
        'E': 129,
        'M': 131,
        'H': 137,
        'F': 147,
        'R': 156,
        'Y': 163,
        'W': 186
    }
    return amino_acid_mass


def linear_spectrum(peptide):
    """
    spectrum of all posible masses that are sub sequences of a linear peptide
    """
    a_mass = aa_mass()
    alphabet = aa_alphabet()

    prefix_mass = {}
    prefix_mass[0] = 0
    for i in range(len(peptide)):
        prefix_mass[i+1] = prefix_mass[i]+a_mass[peptide[i]]

    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i+1, len(prefix_mass)):
            spectrum.append(prefix_mass[j]-prefix_mass[i])

    return sorted(spectrum)


def cyclic_spectrum(peptide):
    """
    spectrum of all posible masses that are sub sequences of cyclic peptide
    """
    a_mass = aa_mass()
    alphabet = aa_alphabet()

    prefix_mass = {}
    prefix_mass[0] = 0
    for i in range(len(peptide)):
        prefix_mass[i+1] = prefix_mass[i]+a_mass[peptide[i]]

    peptide_mass = prefix_mass[len(peptide)]

    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i+1, len(prefix_mass)):
            spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < len(peptide):
                spectrum.append(peptide_mass - (prefix_mass[j]-prefix_mass[i]))
    return sorted(spectrum)


if __name__ == "__main__":

    out = set()
    pep = "VKPWWHAQWGSLS"
    out = cyclic_spectrum(pep)
    out = [str(k) for k in sorted(list(out))]
    print(" ".join(out))

# 0 71 71 99 101 103 113 113 114 128 128 131 147 163 170 172 184 199 215 227 231 244 259 260 266 271 286 298 310 312 330 330 372 385 391 394 399 401 413 423 443 443 493 502 513 519 526 541 554 556 564 590 616 640 654 657 665 682 703 711 753 753 779 785 785 812 824 856 866 884 913 925 926 955 969 984 1012 1039 1056 1083 1083 1097 1154 1170 1184 1196 1255 1267 1298 1368 1369 1482
# 0 71 71 99 101 103 113 113 114 128 128 131 147 163 170 172 184 199 215 227 227 231 244 259 260 266 271 286 298 298 310 312 328 330 330 372 385 391 394 399 399 399 401 413 423 426 443 443 470 493 498 502 513 519 526 527 541 554 556 557 564 569 590 598 616 626 640 654 657 658 665 670 682 697 697 703 711 729 729 753 753 771 779 785 785 800 812 817 824 825 828 842 856 866 884 892 913 918 925 926 928 941 955 956 963 969 980 984 989 1012 1039 1039 1056 1059 1069 1081 1083 1083 1083 1088 1091 1097 1110 1152 1152 1154 1170 1172 1184 1184 1196 1211 1216 1222 1223 1238 1251 1255 1255 1267 1283 1298 1310 1312 1319 1335 1351 1354 1354 1368 1369 1369 1379 1381 1383 1411 1411 1482
