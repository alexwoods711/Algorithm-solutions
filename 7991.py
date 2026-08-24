import ast


def possible_winners(votes, voters):
    max_vote = max(votes)
    max_count = votes.count(max_vote)

    # Find second maximum vote
    second_max = -1
    for v in votes:
        if v != max_vote:
            second_max = max(second_max, v)

    count = 0
    for v in votes:
        if v == max_vote:
            strongest_opponent = second_max if max_count == 1 else max_vote
        else:
            strongest_opponent = max_vote

        if v + voters > strongest_opponent:
            count += 1

    return count


# -------- INPUT HANDLING --------
# Input example:
# [[1, 1, 1, 1], 1]

votes, voters = ast.literal_eval(input().strip())

print(possible_winners(votes, voters))
