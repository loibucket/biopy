from collections import defaultdict


def def_list():
    return []


def debrujin_graph(kmers):
    """
    return an adjacency list from a list of kmers
    """

    dct = defaultdict(def_list)

    links = []

    for mer in kmers:
        dct[mer[0:-1]].append(mer[1:])
        dct[mer[0:-1]].sort()

    for key in dct:
        links.append(key + " -> " + ",".join(dct[key]))

    links.sort()

    return links


if __name__ == "__main__":

    datasets = [["dataset_200_8.txt"], ["dataset_200_quiz.txt"]]
    for i, d in enumerate(datasets):
        with open(d[0], "r") as f:
            kmers = f.read().splitlines()

        links = debrujin_graph(kmers)

        file = open('out_'+str(i)+'.txt', 'w')
        file.write("\n".join(links))
        file.close()
