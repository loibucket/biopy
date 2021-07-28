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
            links.append(mer[0:-1] + "->" + mer[1:])
        return links

    for mer in kmers:
        dct[mer[0:-1]].append(mer[1:])
        dct[mer[0:-1]].sort()

    for mer in dct.keys():
        links.append(mer + "->" + ",".join(dct[mer]))

    return links


def debrujin_reverse(adj_list):
    """
    returns the original kmers formed from the adjacent list
    """
    kmers = []
    for line in adj_list:
        nodes = line.split("->")
        seq = []
        # add the first mer in each node
        for n in nodes:
            seq.append(n[0])
        # add the trailing mers in the last node
        nodelen = len(nodes[0])
        for pos in reversed(range(1, nodelen)):
            seq.append(nodes[-1][-pos])
        kmers.append("".join(seq))
    return kmers


if __name__ == "__main__":

    datasets = [["dataset_200_8.txt"], ["dataset_200_quiz.txt"]]
    for i, d in enumerate(datasets):
        with open(d[0], "r") as f:
            kmers = f.read().splitlines()

        links = debrujin_graph(kmers)

        file = open("out_" + str(i) + ".txt", "w")
        file.write("\n".join(links))
        file.close()
