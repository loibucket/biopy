if __name__ == "__main__":

    #datasets = [["dataset_wk4-2.txt", "dataset_wk4-2a.txt"]]
    datasets = [["dataset_198_3.txt"]]
    for d in datasets:
        with open(d[0], "r") as f:
            lines = f.read().splitlines()
        string = lines[0]
        for l in lines[1:]:
            string += (l[-1])
        print(string)
