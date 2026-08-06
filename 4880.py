import sys
sys.setrecursionlimit(10**7)

MOD = 10007

# fast power mod
def qpow(a, b):
    res = 1
    a %= MOD
    while b:
        if b & 1:
            res = res * a % MOD
        a = a * a % MOD
        b >>= 1
    return res

# Berlekamp–Massey
def berlekamp_massey(s):
    n = len(s)
    C = [0] * n
    B = [0] * n
    C[0] = B[0] = 1
    L, m, b = 0, 0, 1

    for i in range(n):
        m += 1
        d = s[i]
        for j in range(1, L + 1):
            d = (d + C[j] * s[i - j]) % MOD
        if d == 0:
            continue
        T = C[:]
        coef = d * qpow(b, MOD - 2) % MOD
        for j in range(m, n):
            C[j] = (C[j] - coef * B[j - m]) % MOD
        if 2 * L > i:
            continue
        L = i + 1 - L
        B = T
        b = d
        m = 0

    C = C[:L + 1]
    C = [(-x) % MOD for x in C[1:]]
    return C

# Linear recurrence exponentiation
def linear_rec(S, tr, k):
    n = len(tr)

    def combine(a, b):
        res = [0] * (2 * n + 1)
        for i in range(n + 1):
            for j in range(n + 1):
                res[i + j] = (res[i + j] + a[i] * b[j]) % MOD
        for i in range(2 * n, n, -1):
            for j in range(n):
                res[i - 1 - j] = (res[i - 1 - j] + res[i] * tr[j]) % MOD
        return res[:n + 1]

    pol = [0] * (n + 1)
    e = [0] * (n + 1)
    pol[0] = e[1] = 1

    k += 1
    while k:
        if k & 1:
            pol = combine(pol, e)
        e = combine(e, e)
        k >>= 1

    ans = 0
    for i in range(n):
        ans = (ans + pol[i + 1] * S[i]) % MOD
    return ans

# Main DP
def solve():
    s = sys.stdin.readline().strip()
    k = int(sys.stdin.readline())
    n = len(s)

    dp = [[[-1] * 2010 for _ in range(205)] for _ in range(205)]

    def yo(i, j, k):
        if k < 0:
            return 0
        if k == 0 and i >= j:
            return 1
        if dp[i][j][k] != -1:
            return dp[i][j][k]

        if k == 0:
            dp[i][j][k] = int(s[i] == s[j]) * yo(i + 1, j - 1, 0)
            return dp[i][j][k]

        res = 0
        if i > j:
            p = min(k, 2)
            res += 26 * yo(i, j, k - p)
        elif i == j:
            res += yo(i + 1, j, k - 1)
            res += 25 * yo(i, j, k - 2)
        else:
            if s[i] == s[j]:
                res += yo(i + 1, j - 1, k)
                res += 25 * yo(i, j, k - 2)
            else:
                res += yo(i, j - 1, k - 1)
                res += yo(i + 1, j, k - 1)
                res += 24 * yo(i, j, k - 2)

        dp[i][j][k] = res % MOD
        return dp[i][j][k]

    seq = [yo(0, n - 1, i) for i in range(2001)]
    tr = berlekamp_massey(seq)
    seq = seq[:len(tr)]
    print(linear_rec(seq, tr, k))

if __name__ == "__main__":
    solve()



"""
palindrom = lambda s: s == s[::-1]
printans = lambda l: print("".join(l))
s = list(sys.stdin.readline().strip())

for i in range(len(s) + 1):
    for letter in "abcdefghijklmnopqrstvwuxyz":
        tmp = s[:]
        tmp.insert(i, letter)
        if palindrom(tmp):
            printans(tmp)
            exit()

print("NA")
"""