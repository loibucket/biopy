from collections import defaultdict
import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


def defvalue():
    return []


def trim(leaderboard, spectrum, N, mass=bp.aa_mass()):

    scores_map = defaultdict(defvalue)
    for leader in leaderboard:
        scores_map[bp.spectrum_aa_score(leader, spectrum, linear=True)].append(leader)

    new_leaderboard = []
    for s in sorted(scores_map.keys(), reverse=True):
        new_leaderboard += scores_map[s]
        if len(new_leaderboard) >= N:
            break

    return new_leaderboard


if __name__ == "__main__":
    # spec = "0 99 113 114 128 227 257 299 355 356 370 371 484"
    # spec = [int(s) for s in spec.split()]
    # pep = "NQEL"
    # out = bp.spectrum_aa_score(pep, spec, linear=True)
    # print(out)

    # with open("dataset_4913_1.txt") as f:
    #     dataset = f.read().splitlines()
    #     pep = dataset[0]
    #     spec = [int(s) for s in dataset[1].split()]
    # out = bp.spectrum_aa_score(pep, spec, linear=True)
    # print(out)

    peps = "LAST ALST TLLT TQAS"
    peps = peps.split()

    spec = "0 71 87 101 113 158 184 188 259 271 372"
    spec = [int(s) for s in spec.split()]
    N = 2
    out = trim(peps, spec, N)
    print(" ".join(out))

    with open("dataset_4913_3 (1).txt") as f:
        dataset = f.read().splitlines()
        peps = dataset[0].split()
        spec = [int(s) for s in dataset[1].split()]
        N = int(dataset[2])

    out = trim(peps, spec, N)
    print(" ".join(out))
