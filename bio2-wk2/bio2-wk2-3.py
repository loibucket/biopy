

def read_pairs(seq, k, d):

    lst = []
    for i in range(len(seq)-k-d-2):
        b = i + k + d
        lst.append("("+seq[i:(i+k)]+"|"+seq[b:(b+k)]+")")
    lst.sort()
    return("".join(lst))


if __name__ == "__main__":
    seq = "TAATGCCATGGGATGTT"
    k = 3
    d = 2
    print(read_pairs(seq, k, d))
