def min_levels_to_play(possible):
    n = len(possible)
    if n == 0:
        return -1

    alice_points = 0
    bob_points = sum(possible)

    for i in range(n):
        if possible[i] == 1:
            alice_points += 1
            bob_points -= 1
        else:
            alice_points -= 1

        if alice_points > bob_points:
            return i + 1

    return -1



# Test cases
print(min_levels_to_play([1, 0, 1, 0]))  # should output 1
print(min_levels_to_play([1, 1, 1, 1]))  # should output 3
print(min_levels_to_play([0, 0]))  # should output -1
