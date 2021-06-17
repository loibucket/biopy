import biopy as bp
from collections import defaultdict


def defvalue():
    return []


def leaderboard_cyclo_sequence(spectrum, N, nonproteingenic=False, max_loop=30, debug=True):
    """
    find the most probable mass-peptide to fit the spectrum
    """
    if debug:
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
            print("loop", loop, "leader_peptide", len(leader_peptide), leader_peptide[: min(5, N)], "leader_score", leader_score, "leaderboard", len(leaderboard))
        if loop > max_loop:
            break

        leaderboard = bp.expand_peptides(leaderboard, nonproteingenic=nonproteingenic)
        leaderboard_scores = defaultdict(defvalue)

        if debug:
            print("expanded leaderboard", len(leaderboard))

        for i, pep in enumerate(leaderboard):
            if debug and (i + 1) % (100000) == 0:
                print(i + 1)

            masspep = sum(pep)
            if not masspep > parent_mass:

                leaderboard_scores[bp.spectrum_mass_score(pep, spectrum, linear=True)].append(pep)

            if masspep == parent_mass:
                pep_cyclic_score = bp.spectrum_mass_score(pep, spectrum, linear=False)
                if pep_cyclic_score > leader_score:
                    leader_peptide = [pep]
                    leader_score = pep_cyclic_score
                if pep_cyclic_score == leader_score:
                    if pep not in leader_peptide:
                        leader_peptide.append(pep)

        leaderboard = leaderboard_trim(leaderboard_scores, N)

    return leader_peptide


def leaderboard_trim(leaderboard_scores, N, debug=True):
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


if __name__ == "__main__":

    # N = 10
    # # spec = "0 71 113 129 147 200 218 260 313 331 347 389 460"
    # spec = "0 71 113 129 147 200 218 260 313 331 347 389 460"
    # print("N", N, "spec", spec)
    # spec = [int(s) for s in spec.split(" ")]
    # out = leaderboard_cyclo_sequence(spec, N)
    # out = [str(o) for o in out]
    # print("-".join(out))

    # with open("dataset_102_8.txt") as f:
    #     dataset = f.read().splitlines()
    #     N = int(dataset[0])
    #     spec = [int(s) for s in dataset[1].split(" ")]
    #     print("N", N, "spec", spec)
    # out = leaderboard_cyclo_sequence(spec, N)
    # out = [str(o) for o in out]
    # print("-".join(out))

    # out = leaderboard_cyclo_sequence([0,57,58,115], 10, nonproteingenic=True)
    # print(len(out))
    # print(out)

    with open("dataset_103_2.txt") as f:
        dataset = f.read().splitlines()
        N = int(dataset[0])
        spec = [int(s) for s in dataset[1].split()]
    out = bp.leaderboard_cyclo_sequence(spec, N, nonproteingenic=True)

    print(len(out))
    print(out)

    res_set = set()
    for o in out:
        ot = [str(ot) for ot in o]
        res_set.add("-".join(ot))

    print(len(res_set))
    print(" ".join(res_set))
