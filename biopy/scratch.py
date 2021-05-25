# with open("scratch.txt", "r") as f:
#     lines = f.read().splitlines()
#     for l in lines:
#         print(l.split("/")[1])

#     for l in lines:
#         print(l.split("/")[1].split()[1])


with open("scratch-meme.txt", "r") as f:
    lines = f.read().splitlines()
    for l in lines:
        data = l.split()
        print(data[2]+" "+data[5])

    for l in lines:
        data = l.split()
        print(data[5])
