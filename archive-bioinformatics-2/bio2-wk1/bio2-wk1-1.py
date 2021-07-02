import sys

sys.path.insert(0, "../")
sys.path.insert(0, "../../")
import biopy as bp


if __name__ == "__main__":

    # datasets = [["dataset_wk4-2.txt", "dataset_wk4-2a.txt"]]
    datasets = [["../datasets/dataset_197_3.txt"]]
    for d in datasets:
        with open(d[0], "r") as f:
            lines = f.read().splitlines()
            k = int(lines[0])
            seq = lines[1]

        out = bp.all_kmers(seq, k)
        # print("\n".join(out))

        file = open("out.txt", "w")
        file.write("\n".join(out))
        file.close()
