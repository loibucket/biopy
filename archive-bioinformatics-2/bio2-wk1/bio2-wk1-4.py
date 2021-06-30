if __name__ == "__main__":

    binary_list = []
    for i in range(16):
        binary_list.append('{0:04b}'.format(i))

    print(binary_list)

    binary_list = []
    for i in range(pow(2, 5)):
        binary_list.append('{0:010b}'.format(i))

    print(binary_list)
