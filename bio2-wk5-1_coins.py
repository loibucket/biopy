# Code Challenge: Solve the Change Problem. The DPChange pseudocode is reproduced below for your convenience.

# Input: An integer money and an array Coins = (coin1, ..., coind).
# Output: The minimum number of coins with denominations Coins that changes money.
#    DPChange(money, Coins)
#       MinNumCoins(0) ← 0
#       for m ← 1 to money
#          MinNumCoins(m) ← ∞
#          for i ← 0 to |Coins| - 1
#             if m ≥ coini
#                if MinNumCoins(m - coini) + 1 < MinNumCoins(m)
#                   MinNumCoins(m) ← MinNumCoins(m - coini) + 1
#       output MinNumCoins(money)
import math


def dpchange(money, coins):
    min_num_coins = {}
    min_num_coins[0] = 0
    for m in range(1, money + 1):
        min_num_coins[m] = math.inf
        for coin in coins:
            if m >= coin:
                if min_num_coins[m - coin] + 1 < min_num_coins[m]:
                    min_num_coins[m] = min_num_coins[m - coin] + 1
    return min_num_coins[money]


if __name__ == "__main__":

    out = dpchange(30, [1, 5, 10, 25])
    print(out)

    out = dpchange(17155, [21, 19, 16, 9, 8, 5, 3, 1])
    print(out)
