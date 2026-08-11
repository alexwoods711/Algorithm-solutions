import ast
import sys

def max_product(lst, n_largest_elements):
    lst_largest = sorted(lst)[-n_largest_elements:]
    prod = 1
    for number in lst_largest:
        prod *= number
    return prod

s = sys.stdin.readline().strip()
lst, n_largest_elements = ast.literal_eval(s)

print([max_product(lst, n_largest_elements)])