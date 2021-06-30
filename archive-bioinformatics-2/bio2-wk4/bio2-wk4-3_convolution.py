def spectral_convolution(spectrum):
    specq = spectrum[1:].copy()
    convoluted = []
    while specq:
        subtract = specq.pop()
        for s in specq:
            subbed = subtract - s
            if subbed != 0:
                convoluted.append(subbed)
    return sorted(convoluted + spectrum[1:])


if __name__ == "__main__":
    spectrum = "0 137 186 323"
    spectrum = [int(s) for s in spectrum.split()]
    print(spectrum)

    out = spectral_convolution(spectrum)
    print(out)

    # spectrum = "0 71 87 87 113 113 114 115 128 128 158 158 200 215 228 228 241 242 242 245 271 286 315 329 341 355 356 358 370 373 386 400 428 457 469 470 473 483 486 487 499 528 556 570 583 586 598 600 601 615 627 641 670 685 711 714 714 715 728 728 741 756 798 798 828 828 841 842 843 843 869 869 885 956"
    # spectrum = [int(s) for s in spectrum.split()]
    # print(spectrum)

    # out = spectral_convolution(spectrum)
    # out = [str(o) for o in out]
    # print(" ".join(out))

    spectrum = "0 71 87 87 101 115 131 137 186 186 186 188 202 208 218 257 273 287 301 317 323 333 372 374 374 388 394 394 404 410 418 459 481 505 505 509 511 519 519 560 580 582 590 592 596 620 667 691 695 697 705 707 727 768 768 776 778 782 782 806 828 869 877 883 893 893 899 913 913 915 954 964 970 986 1000 1014 1030 1069 1079 1085 1099 1101 1101 1101 1150 1156 1172 1186 1200 1200 1216 1287"
    spectrum = [int(s) for s in spectrum.split()]
    print(spectrum)

    out = spectral_convolution(spectrum)
    out = [str(o) for o in out]
    print(" ".join(out))
