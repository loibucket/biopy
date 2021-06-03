import biopy as bp


def pairs_adj_list(k, pairs):
    """
    creates an adjacency list from read-pairs
    """
    kmers_top = []
    kmers_bot = []
    for pair in pairs:
        kmers_top.append(pair[:k])
        kmers_bot.append(pair[k + 1:])
    deb_top_links = bp.debrujin_graph(kmers_top, sort=False)
    deb_bot_links = bp.debrujin_graph(kmers_bot, sort=False)
    assert (len(deb_top_links) == len(deb_bot_links))
    deb_links = {}
    adj_list = []
    for i in range(len(deb_top_links)):
        top = deb_top_links[i].split(" -> ")
        bot = deb_bot_links[i].split(" -> ")
        deb_key = top[0] + "|" + bot[0]
        deb_links[deb_key] = top[1] + "|" + bot[1]
        adj_list.append(deb_key + " -> " + deb_links[deb_key])
    return adj_list


def pairs_reconstruct(k, d, pairs):
    """
    reconstruct read-pairs into list of kmers
    """
    k, d = int(k), int(d)
    fullpairs = []
    for pair in pairs:
        full = pair[:k - 1] + "x" * d + pair[k:]
        fullpairs.append(full)
    return fullpairs


def seq_reconstruct(k, d, kmers):
    """
    reconstruct list of kmers into sequence
    """
    seq = []
    for p in kmers:
        seq.append(p[0])
    for i in reversed(range(1, 2 * k + d - 1)):
        seq.append(kmers[-i][-1])
    return ("".join(seq))


def string_reconstruct(k, d, pairs):
    """
    reconstruct sequence from read-pairs
    """
    adj_list = pairs_adj_list(k, pairs)
    eul_pairs = bp.euler_cycle(adj_list)
    kmers = pairs_reconstruct(k, d, eul_pairs)
    seq = seq_reconstruct(k, d, kmers)
    return seq


if __name__ == "__main__":
    files = ["dataset-wk2-4.txt", "dataset_204_16.txt"]
    for i, dataset in enumerate(files):
        with open(dataset) as file:
            data = file.read().splitlines()
            kk, dd = data[0].split(" ")
            kk, dd = int(kk), int(dd)
            pp = data[1:]

        ss = string_reconstruct(kk, dd, pp)
        # print(seq)
        # print("GTGGTCGTGAGATGTTGA")

        file = open('out_' + str(i) + '.txt', 'w')
        file.write(ss)
        file.close()
