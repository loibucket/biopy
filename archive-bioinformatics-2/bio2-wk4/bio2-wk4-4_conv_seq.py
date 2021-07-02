from collections import defaultdict
import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


def defvalue():
    return []


def convolution_cyclo_sequence(spectrum, N=100, M=100, debug=True):
    """
    get the most probable peptides from the spectrum
    N: leaderboard trim limit
    M: convolutions trim limit
    """
    conv = bp.spectral_convolution(spectrum)
    conv_map = bp.spectral_convolution_map(conv)
    mass_list = bp.leaderboard_trim(conv_map, M)
    mass_list.sort()

    if debug:
        print("convolution_cyclo_sequence-py")
        print("spectrum", spectrum)
        print("conv", len(conv))
        print("conv_map", conv_map)
        print("mass_list", len(mass_list), mass_list)

    return bp.leaderboard_cyclo_sequence(spectrum, N, mass_list=mass_list)


if __name__ == "__main__":

    # M = 20
    # N = 60
    # spectrum = "57 57 71 99 129 137 170 186 194 208 228 265 285 299 307 323 356 364 394 422 493"
    # spectrum = sorted([int(s) for s in spectrum.split()])
    # out = convolution_cyclo_sequence(spectrum, N, M)
    # print(out)
    # for o in out:
    #     print("-".join([str(ot) for ot in o]))

    with open("Tyrocidine_Experimental.txt") as f:
        dataset = f.read().splitlines()
        M = 50
        N = 1000
        spectrum = dataset[0]

    spectrum = [int(round(float(s))) for s in spectrum.split()]
    out = bp.convolution_cyclo_sequence(spectrum, N, M)
    print(out)

    for o in out:
        print(" ".join([str(ot) for ot in o]))
    print("")
    print(len(out))


# 130 97 165 113 131 82 161 129 164 97
# 130 97 165 113 131 82 161 129 181 80
# 161 82 147 163 99 97 130 145 81 64 100
# 130 97 163 115 131 146 97 145 83 65 97
