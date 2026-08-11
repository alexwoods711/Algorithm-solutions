from math import floor, exp
import sys
import ast


def ex_euler(n):
    F = lambda t, y: 2 - exp(-4 * t) - 2 * y
    t0 = 0
    y0 = 1
    T = 1
    h = T / float(n)
    X = [t0]
    Y = [y0]
    Z = []
    R = []
    for k in range(0, n):
        X.append((k + 1) * h)
        Y.append(Y[k] + h * F(X[k], Y[k]))
    for k in range(0, n + 1):
        Z.append(1 + 0.5 * exp(-4 * X[k]) - 0.5 * exp(-2 * X[k]))
        R.append(abs(Y[k] - Z[k]) / float(Z[k]))
    return floor(sum(R) / float(n + 1) * 1000000.0) / 1000000.0


s = sys.stdin.readline().strip()
n = ast.literal_eval(s)[0]

print([ex_euler(n)])
