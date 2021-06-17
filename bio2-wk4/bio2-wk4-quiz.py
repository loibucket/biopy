import biopy as bp


if __name__ == "__main__":

    pep = "MAMA"
    spectrum = "0 71 98 99 131 202 202 202 202 202 299 333 333 333 503"
    spectrum = [int(s) for s in spectrum.split()]
    out = bp.spectrum_aa_score(pep, spectrum, linear=False)
    print(out)

    pep = "PEEP"
    spectrum = "0 97 97 97 100 129 194 226 226 226 258 323 323 355 393 452"
    spectrum = [int(s) for s in spectrum.split()]
    out = bp.spectrum_aa_score(pep, spectrum, linear=True)
    print(out)

    spectrum = "0 57 118 179 236 240 301"
    spectrum = [int(s) for s in spectrum.split()]
    con = bp.spectral_convolution(spectrum)
    con_map = bp.spectral_convolution_map(con)
    print(con_map)
