def ham_dist(p, q):
    count = 0
    for i in range(len(p)):
        if p[i] != q[i]:
            count += 1
    return count


def approx_match(d, seq, mer):
    print("seq", len(seq), seq[:10], seq[-10:])
    count = 0
    for i in range(len(seq)-len(mer)+1):
        if ham_dist(mer, seq[i:i+len(mer)]) <= d:
            count += 1
    return count


if __name__ == "__main__":

    with open("dataset_9_4.txt", "r") as f:
        (mer, seq, d) = f.read().splitlines()
        d = int(d)

    with open("dataset_9_4.txt", "r") as f:
        merx = f.readline().rstrip()
        seqx = f.readline().rstrip()
        dx = int(f.readline().rstrip())

    sample = [
        # (d, seq, mer),
        # (dx, seqx, merx),
        (2, "CATGCCATTCGCATTGTCCCAGTGA", "CCC"),
        (2, "TTTAGAGCCTTCAGAGG", "GAGG"),
        (2, "ATTGGGATAGGCATATGCGATAAAAGCCCCCCCAACCTCATAACGGAGTGCGAACATGCTGGACAATGTCCGCTTCGGAAAGAACGCGGAAACACGTACCCAAAGTCATAAGACCACGCCACGGTATTTTATTAAGCAAATTGAGGTACAGCCATTTCGGAATACTAGACGACCTAACCATCGGCGACAAACGCCGACTAATCCTTCTAAAAATAATATCCTATACTAAGGCTGGTATCAGGCACCCAGGCACTCGAGGTGACTTCGCCGTGGTCACAAAGAACCAAGACCTAGCGACCTGGATATCCTCCATCCGGCTT", "GAACGCG"),
    ]

    for s in sample:
        print(approx_match(*s))
