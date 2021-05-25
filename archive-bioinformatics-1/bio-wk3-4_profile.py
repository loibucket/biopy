

def pr(seq, profile):
    prob = 1
    for i, char in enumerate(seq):
        prob *= profile[char][i]
    return prob


def kmers(seq, k):
    """
    find all the kmers in seq
    """
    kmers = set()
    for i in range(len(seq)-k+1):
        kmers.add(seq[i:i+k])
    return kmers


def mostPr(seq, k, profile):
    km = kmers(seq, k)
    score = 0
    median = ""
    for kmer in km:
        p = pr(kmer, profile)
        if p > score:
            score = p
            median = kmer
    if median == "":
        return seq[0:k]
    return median


if __name__ == "__main__":

    profile = {
        'A': [0.2, 0.2, 0.0, 0.0, 0.0, 0.0, 0.9, 0.1, 0.1, 0.1, 0.3, 0.0],
        'C': [0.1, 0.6, 0.0, 0.0, 0.0, 0.0, 0.0, 0.4, 0.1, 0.2, 0.4, 0.6],
        'G': [0.0, 0.0, 1.0, 1.0, 0.9, 0.9, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0],
        'T': [0.7, 0.2, 0.0, 0.0, 0.1, 0.1, 0.0, 0.5, 0.8, 0.7, 0.3, 0.4]
    }

    #print(pr("ACGGGGATTACC", profile))
    #print(pr("TCGTGGATTTCC", profile))

    profile = {
        'A': [0.4, 0.3, 0.0, 0.1, 0.0, 0.9],
        'C': [0.2, 0.3, 0.0, 0.4, 0.0, 0.1],
        'G': [0.1, 0.3, 1.0, 0.1, 0.5, 0.0],
        'T': [0.3, 0.1, 0.0, 0.4, 0.5, 0.0]
    }

    print(pr("AAGTTC", profile))

    profile = {
        'A': [0.2, 0.2, 0.3, 0.2, 0.3],
        'C': [0.4, 0.3, 0.1, 0.5, 0.1],
        'G': [0.3, 0.3, 0.5, 0.2, 0.4],
        'T': [0.1, 0.2, 0.1, 0.1, 0.2]
    }

    print(mostPr("ACCTGTTTATTGCCTAAGTTCCGAACAAACCCAATATAGCCCGAGGGCCT", 5, profile))

    print("test")
    profile = {'A': [0, 0, 0], 'C': [0, 0, 1.0], 'G': [1.0, 1.0, 0], 'T': [0, 0, 0]}
    print(mostPr("AAGAATCAGTCA", 3, profile))

    with open("dataset_159_3.txt", "r") as f:
        lines = f.read().splitlines()
        seq = lines[0]
        k = int(lines[1])
        profile = {}
        profile['A'] = [float(x) for x in lines[2].split(" ")]
        profile['C'] = [float(x) for x in lines[3].split(" ")]
        profile['G'] = [float(x) for x in lines[4].split(" ")]
        profile['T'] = [float(x) for x in lines[5].split(" ")]

    print(mostPr(seq, k, profile))
