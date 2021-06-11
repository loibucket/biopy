import biopy as bp

if __name__ == "__main__":
    files = ["dataset-wk2-4x.txt", "dataset-wk2-4.txt"]  # "dataset_6206_4.txt"]
    for i, dataset in enumerate(files):
        with open(dataset) as file:
            data = file.read().splitlines()
            kk, dd = data[0].split(" ")
            kk, dd = int(kk), int(dd)
            pp = data[1:]

        seq = bp.pairs_to_sequence(kk, dd, pp, debug=True)
        print("out", seq, len(seq))
        ans = ["GACCGAGCGCCGGA", "GTGGTCGTGAGATGTTGA"]
        print("ans", ans[i], len(ans[i]))

        file = open('out_' + str(i) + '.txt', 'w')
        file.write(seq)
        file.close()
