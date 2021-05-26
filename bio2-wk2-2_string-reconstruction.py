from biopy.euler_cycle import euler_cycle
import biopy as bp
import itertools


def string_reconstruction(patterns):
    k = len(patterns[0])
    adjacency_list = bp.debrujin_graph(patterns)
    euler = euler_cycle(adjacency_list)
    seq = euler[0]
    for kmer in euler[1:]:
        seq += kmer[-1]
    return seq


def universal_string(k):
    binary_strings = ["".join(i) for i in itertools.product('01', repeat=k)]
    adjacency_list = bp.debrujin_graph(binary_strings)
    euler = euler_cycle(adjacency_list)
    seq = euler[-1]
    for kmer in euler[:-k]:
        seq += kmer[-1]
    return seq


if __name__ == "__main__":

    val = universal_string(2)
    print(val, len(val))

    datasets = ["dataset_203_7-sample.txt", "dataset_203_7-2.txt"]
    for i, d in enumerate(datasets):
        with open(d, "r") as f:
            data = f.read().splitlines()
            kmers = data[1:]

            seq = string_reconstruction(kmers)
            print(seq)

            file = open('out_'+str(i)+'.txt', 'w')
            file.write(seq)
            file.close()
