import sys
import ast
import re

TACODICT = {
    "t": "tomato",
    "l": "lettuce",
    "c": "cheese",
    "g": "guacamole",
    "s": "salsa",
}


def tacofy(word):
    return (
        ["shell"]
        + [TACODICT.get(c, "beef") for c in re.sub("[^aeioutlcgs]+", "", word.lower())]
        + ["shell"]
    )


input_str = sys.stdin.readline().strip()
input_data = ast.literal_eval(input_str)
output = tacofy(*input_data)
print([output])