from collections import defaultdict


def defvalue():
    return []


def mass_list():
    return [57, 71, 87, 97, 99, 101, 103, 113, 114, 115, 128, 129, 131, 137, 147, 156, 163, 186]


def spectral_convolution(spectrum):
    """
    get the positive difference between all numbers
    """
    specq = spectrum.copy()
    specq.sort()
    if specq[0] != 0:
        speq = [0] + specq
    convoluted = []
    while specq:
        subtract = specq.pop()
        for s in specq:
            subbed = subtract - s
            if subbed != 0:
                convoluted.append(subbed)
    return convoluted


def spectral_convolution_map(convolutions):
    """
    map the convolution by count
    """
    conv_map = defaultdict(defvalue)
    uniques = set(convolutions.copy())
    for u in uniques:
        if u >= 57 and u <= 200:
            conv_map[convolutions.count(u)].append(u)

    return conv_map


def leaderboard_trim(leaderboard_scores, N, debug=False):
    """
    trim leaderboard to top N players
    """
    if leaderboard_scores == []:
        return []

    new_leaderboard = []
    for score in sorted(leaderboard_scores.keys(), reverse=True):
        new_leaderboard += leaderboard_scores[score]
        if debug:
            print("score", score, "players", len(leaderboard_scores[score]), "new_leaderboard", len(new_leaderboard))
        if len(new_leaderboard) >= N:
            return new_leaderboard
    return new_leaderboard


def linear_mass_spectrum(peptide):
    """
    spectrum of all posible masses that are sub sequences of a linear peptide
    """

    prefix_mass = {}
    prefix_mass[0] = 0
    for i in range(len(peptide)):
        prefix_mass[i + 1] = prefix_mass[i] + peptide[i]

    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i + 1, len(prefix_mass)):
            spectrum.append(prefix_mass[j] - prefix_mass[i])

    return sorted(spectrum)


def cyclo_mass_spectrum(peptide):
    """
    spectrum of all posible masses that are sub sequences of cyclic peptide
    """

    prefix_mass = {}
    prefix_mass[0] = 0
    for i in range(len(peptide)):
        prefix_mass[i + 1] = prefix_mass[i] + peptide[i]

    peptide_mass = prefix_mass[len(peptide)]

    spectrum = [0]
    for i in range(len(prefix_mass)):
        for j in range(i + 1, len(prefix_mass)):
            spectrum.append(prefix_mass[j] - prefix_mass[i])
            if i > 0 and j < len(peptide):
                spectrum.append(peptide_mass - (prefix_mass[j] - prefix_mass[i]))
    return sorted(spectrum)


def spectrum_mass_score(peptide, input_spectrum, linear=False):
    """
    find the score of a spectrum against a given peptide, as a mass sequence
    """
    if not input_spectrum:
        return 0

    spectrum = input_spectrum.copy()

    if linear:
        test = linear_mass_spectrum(peptide)
    else:
        test = cyclo_mass_spectrum(peptide)

    score = 0
    t = test.pop()
    s = spectrum.pop()

    while t != -1:
        if t == s:
            score += 1
            t = test.pop() if test else -1
            s = spectrum.pop() if spectrum else -1
        elif t < s:
            s = spectrum.pop() if spectrum else -1
        elif t > s:
            t = test.pop() if test else -1

    return score


def expand_peptides(peptides, nonproteingenic=False, mass_list=mass_list()):
    """
    a new collection containing all possible extensions of peptides in Peptides by a single amino acid mass
    """
    if nonproteingenic:
        mass_list = list(range(57, 201))

    new_peptides = []
    for p in peptides:
        for a_mass in mass_list:
            new_peptides.append(p + [a_mass])
    return new_peptides


def leaderboard_cyclo_sequence(spectrum, N, nonproteingenic=False, mass_list=mass_list(), max_loop=30, debug=True):
    """
    find the most probable mass-peptide to fit the spectrum
    """
    if debug:
        print("leaderboard_cyclo_sequence-py")
        print("N", N)
        print("spectrum", spectrum)

    parent_mass = max(spectrum)
    leaderboard = [[]]
    leader_peptide = []
    leader_score = 0

    linear_score_map = {}
    cyclic_score_map = {}
    pep_mass_map = {}

    loop = 0
    while leaderboard:
        loop += 1

        if debug:
            print("loop", loop, "leader_peptide", len(leader_peptide), leader_peptide[:1], "leader_score", leader_score, "leaderboard", len(leaderboard))
        if loop > max_loop:
            break

        leaderboard = expand_peptides(leaderboard, nonproteingenic=nonproteingenic, mass_list=mass_list)
        leaderboard_scores = defaultdict(defvalue)

        if debug:
            print("expanded leaderboard", len(leaderboard), "sample", leaderboard[:1])

        for i, pep in enumerate(leaderboard):
            if debug and (i + 1) % (100000) == 0:
                print(i + 1)

            masspep = sum(pep)
            if not masspep > parent_mass:
                leaderboard_scores[spectrum_mass_score(pep, spectrum, linear=True)].append(pep)

            if masspep == parent_mass:
                pep_cyclic_score = spectrum_mass_score(pep, spectrum, linear=False)
                if pep_cyclic_score > leader_score:
                    leader_peptide = [pep]
                    leader_score = pep_cyclic_score
                if pep_cyclic_score == leader_score:
                    if pep not in leader_peptide:
                        leader_peptide.append(pep)

        leaderboard = leaderboard_trim(leaderboard_scores, N)

    return leader_peptide


def convolution_cyclo_sequence(spectrum, N=100, M=100, debug=True):
    """
    get the most probable peptides from the spectrum
    N: leaderboard trim limit
    M: convolutions trim limit
    """
    conv = spectral_convolution(spectrum)
    conv_map = spectral_convolution_map(conv)
    mass_list = leaderboard_trim(conv_map, M)
    mass_list.sort()

    if debug:
        print("convolution_cyclo_sequence-py")
        print("spectrum", spectrum)
        print("conv", len(conv))
        print("conv_map", conv_map)
        print("mass_list", len(mass_list), mass_list)

    return leaderboard_cyclo_sequence(spectrum, N, mass_list=mass_list)


if __name__ == "__main__":

    with open("dataset_104_8.txt") as f:
        dataset = f.read().splitlines()
        M = int(dataset[0])
        N = int(dataset[1])
        spectrum = dataset[2]

    spectrum = [int(s) for s in spectrum.split()]
    out = convolution_cyclo_sequence(spectrum, N, M)

    for o in out:
        print("-".join([str(ot) for ot in o]), end=" ")
    print("")
    print(len(out))
