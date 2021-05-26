from collections import defaultdict
import biopy as bp
from collections import defaultdict


def def_list():
    return []


def overlap_graph(seq, k):
    """
    build an adjancency list of kmers from a seqeuence 
    """
    kmers = bp.all_kmers(seq, k)

    dct = defaultdict(def_list)

    links = []

    for mer in kmers:
        if mer[0:-1] != mer[1:]:
            dct[mer[0:-1]].append(mer[1:])
            dct[mer[0:-1]].sort()

    for key in dct:
        links.append(key + " -> " + ",".join(dct[key]))

    links.sort()

    return links


if __name__ == "__main__":

    # datasets = [["dataset_wk4-2.txt", "dataset_wk4-2a.txt"]]
    datasets = [["dataset_199_6.txt"]]
    for d in datasets:
        with open(d[0], "r") as f:
            (k, seq) = f.read().splitlines()

        links = overlap_graph(seq, int(k))

        file = open('out.txt', 'w')
        file.write("\n".join(links))
        file.close()
