import sys
import ast

def checkered_board(n):
    if not isinstance(n, int) or n <= 1:
        return False

    board = "\n".join(
        " ".join(
            "\u25a0" if (x + y) % 2 == 0 else "\u25a1"
            for y in range(n)
        )
        for x in range(n)
    )
    return board


input_str = sys.stdin.readline().strip()
input_data = ast.literal_eval(input_str)

output = checkered_board(input_data[0])

# IMPORTANT: wrap in list
print([output])