def skew(seq):
    sk = [0]
    for char in seq:
        if char == "G":
            sk.append(sk[-1]+1)
        elif char == "C":
            sk.append(sk[-1]-1)
        else:
            sk.append(sk[-1])

    m = max(sk)
    lst = [str(i) for i in range(len(sk)) if sk[i] == m]
    return " ".join(lst)


if __name__ == "__main__":

    with open("dataset_7_10.txt", "r") as f:
        data = f.read()

    seq = [
        "GCATACACTTCCCAGTAGGTACTG",
        "ACCG",
        "ACCC",
        data
    ]

    for s in seq:
        print(skew(s))
