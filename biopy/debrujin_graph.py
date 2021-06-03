from collections import defaultdict


def def_list():
    return []


def debrujin_graph(kmers, sort=True):
    """
    return an adjacency list from a list of kmers
    """

    dct = defaultdict(def_list)

    links = []

    if not sort:
        for mer in kmers:
            links.append(mer[0:-1] + " -> " + mer[1:])
        return links

    for mer in kmers:
        dct[mer[0:-1]].append(mer[1:])
        dct[mer[0:-1]].sort()

    for mer in dct.keys():
        links.append(mer + " -> " + ",".join(dct[mer]))

    return links


if __name__ == "__main__":

    datasets = [["dataset_200_8.txt"], ["dataset_200_quiz.txt"]]
    for i, d in enumerate(datasets):
        with open(d[0], "r") as f:
            kmers = f.read().splitlines()

        links = debrujin_graph(kmers)

        file = open('out_' + str(i) + '.txt', 'w')
        file.write("\n".join(links))
        file.close()
