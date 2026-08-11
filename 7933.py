import sys
import ast


def combine_from_input(input_str):
    strings = ast.literal_eval(input_str)  # parse the input string safely

    result = []
    max_len = max(len(s) for s in strings)

    for i in range(max_len):
        for s in strings:
            if i < len(s):
                result.append(s[i])

    combined = "".join(result)
    return str([combined])


print(sys.stdin.readline().strip())
