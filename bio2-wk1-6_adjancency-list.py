from collections import defaultdict
import biopy as bp


def def_list():
    return []


def debrujin_kmers(kmers):
    """
    return an adjacency list from a list of kmers
    """

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
    datasets = [["dataset_200_8.txt"], ["dataset_200_quiz.txt"]]
    for i, d in enumerate(datasets):
        with open(d[0], "r") as f:
            kmers = f.read().splitlines()

        links = debrujin_kmers(kmers)

        file = open('out_'+str(i)+'.txt', 'w')
        file.write("\n".join(links))
        file.close()

    print(bp.all_kmers("0111010001", 3))
    print(bp.all_kmers("1100011011", 3))
    print(bp.all_kmers("0101010100", 3))
    print(bp.all_kmers("1111000111", 3))
    print(bp.all_kmers("0100011101", 3))
    print(bp.all_kmers("0011101000", 3))
