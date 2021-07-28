import biopy as bp
import re


def pairs_to_sequence(k, d, pairs, debug=False):
    """
    fully reconstruct sequence from unordered read-pairs
    """

    if debug:
        print("pairs", pairs)

    # build debrujin graph from read pairs
    deb = bp.pairs_to_debrujin(k, pairs)

    # find euler paths from debrujin graph
    eul_candidates = bp.euler_cycle_all(deb, debug)

    all_seqs = []
    for eul in eul_candidates:

        # convert euler path to ordered debrujin graph
        ord_deb = bp.eul_to_debrujin(eul)

        # convert ordered debrujin graph to ordered read pairs
        ord_pairs = bp.debrujin_to_pairs(ord_deb)

        if debug:
            print("order", ord_pairs)

        # find sequence from ordered read pairs
        seq = bp.ord_pairs_to_sequence(k, d, ord_pairs, debug)

        if seq and seq not in all_seqs:
            all_seqs.append(seq)

    return all_seqs


def ord_pairs_to_sequence(k, d, pairs, debug=False):
    """
    assemble sequence from ordered read-pairs
    return blank if no assembled sequence
    """

    # build seq from initial kmers
    fseq = []
    for p in pairs[:-1]:
        fseq.append(p[0])
    for pos in range(k):
        fseq.append(pairs[-1][pos])

    # build seq from terminal kmers
    rseq = []
    for p in reversed(pairs[1:]):
        rseq = [p[-1]] + rseq
    for pos in range(1, k + 1):
        rseq = [pairs[0][-pos]] + rseq

    if debug:
        print("fseq", "".join(fseq))
    if debug:
        print("rseq", (k + d) * " " + "".join(rseq))

    for pos in range(k + d + 1, len(fseq)):
        if fseq[pos] != rseq[pos - k - d]:
            if debug:
                print("not a sequence")
            return ""

    if debug:
        print("is a sequence")
    return "".join((fseq + rseq[-k - d :]))


def pairs_to_debrujin(k, pairs):
    """
    creates an adjacency list from read-pairs e.g. ['AGA|AGA','TGA|TGA'] to ['AG|AG->GA|GA','TG|TG->GA|GA']
    """
    kmers_top = []
    kmers_bot = []
    for pair in pairs:
        kmers_top.append(pair[:k])
        kmers_bot.append(pair[k + 1 :])
    deb_top_links = bp.debrujin_graph(kmers_top, sort=False)
    deb_bot_links = bp.debrujin_graph(kmers_bot, sort=False)
    assert len(deb_top_links) == len(deb_bot_links)
    deb_links = {}
    adj_list = []
    for i in range(len(deb_top_links)):
        top = deb_top_links[i].split("->")
        bot = deb_bot_links[i].split("->")
        deb_key = top[0] + "|" + bot[0]
        deb_links[deb_key] = top[1] + "|" + bot[1]
        adj_list.append(deb_key + "->" + deb_links[deb_key])
    return adj_list


def debrujin_to_pairs(adj_list):
    """
    convert an debrujin adj list into read pairs eg. ['AG|AG->GA|GA','TG|TG->GA|GA'] to ['AGA|AGA','TGA|TGA']
    """
    ordpairs = []
    for a in adj_list:
        g = re.split("->|\|", a)
        ordpairs.append(g[0] + g[2][-1] + "|" + g[1] + g[3][-1])
    return ordpairs


def eul_to_debrujin(eul):
    """
    build debrujin graph adj list from ordered euler list e.g. ['AG|AG','TC|TC','GG|GG'] to ['AG|AG->TC|TC','TC|TC->GG|GG']
    """
    adj = []
    for i, _ in enumerate(eul[:-1]):
        adj.append(eul[i] + "->" + eul[i + 1])
    return adj


if __name__ == "__main__":
    files = ["dataset-wk2-4.txt", "dataset_204_16.txt"]
    for i, dataset in enumerate(files):
        with open(dataset) as file:
            data = file.read().splitlines()
            kk, dd = data[0].split(" ")
            kk, dd = int(kk), int(dd)
            pp = data[1:]

        ss = pairs_to_sequence(kk, dd, pp)
        # print(seq)
        # print("GTGGTCGTGAGATGTTGA")

        file = open("out_" + str(i) + ".txt", "w")
        file.write(ss)
        file.close()
