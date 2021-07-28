import copy


def two_break_genome_graph_alt(graph, breaks):
    """
    transform a genome graph with the given breaks
    """

    i1 = breaks[0]
    i2 = breaks[1]
    i3 = breaks[2]
    i4 = breaks[3]

    new_g = copy.deepcopy(graph)

    for i in range(len(graph)):

        compare = graph[i]

        if compare == (i1, i2) or compare == (i2, i1):

            if i - 1 > -1:
                if graph[i - 1][1] + 1 == i2 or graph[i - 1][1] - 1 == i2:
                    new_g[i] = (i2, i4)
                else:
                    new_g[i] = (i4, i2)
                continue

            if i + 1 < len(graph):
                if graph[i + 1][0] + 1 == i4 or graph[i + 1][0] == i4:
                    new_g[i] = (i2, i4)
                else:
                    new_g[i] = (i4, i2)
                continue

        if compare == (i3, i4) or compare == (i4, i3):

            if i - 1 > -1:
                if graph[i - 1][1] + 1 == i1 or graph[i - 1][1] - 1 == i1:
                    new_g[i] = (i1, i3)
                else:
                    new_g[i] = (i3, i1)
                continue

            if i + 1 < len(graph):
                if graph[i + 1][0] + 1 == i3 or graph[i + 1][0] == i3:
                    new_g[i] = (i1, i3)
                else:
                    new_g[i] = (i3, i1)
                continue

    return new_g


def two_break_genome_graph(graph, breaks):
    """
    transform a genome graph with the given breaks
    """

    i1 = breaks[0]
    i2 = breaks[1]
    i3 = breaks[2]
    i4 = breaks[3]

    new_g = copy.deepcopy(graph)

    for i in range(len(graph)):

        compare = graph[i]

        if compare == (i1, i2):
            new_g[i] = (i4, i2)
            continue

        if compare == (i2, i1):
            new_g[i] = (i2, i4)
            continue

        if compare == (i3, i4):
            new_g[i] = (i3, i1)
            continue

        if compare == (i4, i3):
            new_g[i] = (i1, i3)
            continue

    return new_g


if __name__ == "__main__":

    graph = "(2, 4), (3, 8), (7, 5), (6, 1)"
    breaks = "1, 6, 3, 8"

    # with open("dataset_8224_2.txt") as f:
    #     dataset = f.read().splitlines()
    #     graph = dataset[0]
    #     breaks = dataset[1]

    # convert string into list of tuples
    graph = [(int(i.split(", ")[0]), int(i.split(", ")[1])) for i in graph[1:-1].split("), (")]

    breaks = [int(i) for i in breaks.split(", ")]

    out = two_break_genome_graph_alt(graph, breaks)

    print(out)

    out = two_break_genome_graph(graph, breaks)

    print(out)
