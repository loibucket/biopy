def overlap_graph(kmers):
    links = []

    for i, imer in enumerate(kmers):

        childs = []
        for j, jmer in enumerate(kmers):
            if i != j:
                if imer[1:] == jmer[0:-1]:
                    childs.append(jmer)

        if childs:
            links.append(imer + "->" + ",".join(childs))

    return links


if __name__ == "__main__":

    # datasets = [["dataset_wk4-2.txt", "dataset_wk4-2a.txt"]]
    datasets = [["dataset_198_10a.txt"]]
    for d in datasets:
        with open(d[0], "r") as f:
            kmers = f.read().splitlines()

        links = overlap_graph(kmers)

        file = open('out.txt', 'w')
        file.write("\n".join(links))
        file.close()
