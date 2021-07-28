def back_step(a, b, sum):

    if sum == 0:
        return 1
    if sum < 0:
        return 0

    return back_step(a, b, sum - a) + back_step(a, b, sum - b)


if __name__ == "__main__":

    out = back_step(2, 3, 24)
    print(out)
