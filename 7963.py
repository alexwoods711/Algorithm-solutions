import sys
import ast
from math import ceil, log10


def graceful_tipping(bill):
    bill *= 1.15
    if bill < 10:
        return ceil(bill)
    e = int(log10(bill))
    unit = 10**e / 2
    return ceil(ceil(bill / unit) * unit)


s = sys.stdin.readline().strip()
bill = ast.literal_eval(s)

print([graceful_tipping(int(bill[0]))])