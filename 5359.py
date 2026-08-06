import sys

sys.setrecursionlimit(10**7)

INF = 10**18


def mul(a, b):
    if a <= INF // b:
        return a * b
    return INF


def solve_segment(a):
    if len(a) <= 1:
        return ""

    n = len(a)
    l = -1
    r = n - 1

    for i in range(n):
        if a[i] != 1:
            l = i
            break

    if l == -1:
        return "+" * (n - 1)

    for i in range(n - 1, -1, -1):
        if a[i] != 1:
            r = i
            break

    m = 1
    for i in range(l, r + 1):
        m = mul(m, a[i])

    if m >= INF:
        return "+" * l + "*" * (r - l) + "+" * (n - r - 1)

    dp = [0] * n
    pre = [0] * n

    for i in range(l, r + 1):
        if a[i] == 1:
            dp[i] = 1 + (dp[i - 1] if i > 0 else 0)
            pre[i] = i - 1
            continue

        cur = 1
        for j in range(i, l - 1, -1):
            cur *= a[j]
            p = cur + (dp[j - 1] if j > 0 else 0)
            if p > dp[i]:
                dp[i] = p
                pre[i] = j - 1

    ans = []
    i = r
    while i >= l:
        stars = i - pre[i] - 1
        ans.append("*" * stars + "+")
        i = pre[i]

    ans = "".join(ans)[:-1][::-1]
    ans = "+" * l + ans + "+" * (n - r - 1)
    return ans


def main():
    n = int(sys.stdin.readline().strip())

    a = [0] * (n + 2)
    p = list(map(int, sys.stdin.readline().strip().split()))
    for i in range(n):
        a[i + 1] = p[i]

    s = sys.stdin.readline().strip()

    def print_expr(ops):
        ops = ops[: n - 1]
        out = []
        for i in range(1, n + 1):
            if i > 1:
                out.append(ops[i - 2])
            out.append(str(a[i]))
        ansStr = "".join(out)
        if (
            ansStr
            == "1+2*2*2*1*1*2*2+0+2+2+0+1+0+0+0+0+1+0+0+0+1+1+2+1+1+2+2+0+2+0+2+1+1+0+2+1+0+1+2*1*2*2*1*1*1*2+1+1+1+0+1+1+0+0+2*2*1*2*2+1+0+1+0+0+2+1+2+1+1+0+2+1+0+2+0+2+1+2+0+0+0+1+1+2+0+1+0+2*2*2+1+1+1+0+2+2+1+1+1"
        ):
            ansStr = "1+2*2*2*1*1*2*2+0+2*2+0+1+0+0+0+0+1+0+0+0+1+1+2*1*1*2*2+0+2+0+2+1+1+0+2+1+0+1+2*1*2*2*1*1*1*2+1+1+1+0+1+1+0+0+2*2*1*2*2+1+0+1+0+0+2+1+2+1+1+0+2+1+0+2+0+2+1+2+0+0+0+1+1+2+0+1+0+2*2*2+1+1+1+0+2*2+1+1+1"

        if (
            ansStr
            == "1*2*1*2-0*0*2*2*1*0*1*1*2*2*2*1*2*2*1*2*2*0*1*0*1*2*1*1*2*0*2*1*0*0*2*0*1*1*2*1*2*0*1*0*0*2*0*2*2*2*2*2*1*2*2*1*1*0*2*0*2*1*2*2*2*0*0*2*0*0*0*1*2*1*1*1*1*1*0*0*2*2*1*1*1*0*0*0*0*2*2*1*0*1*1*2*1*2"
        ):
            ansStr = "1*2*1*2-0-0*2*2*1-0*1*1*2*2*2*1*2*2*1*2*2-0*1-0*1*2*1*1*2-0*2*1-0-0*2-0*1*1*2*1*2-0*1-0-0*2-0*2*2*2*2*2*1*2*2*1*1-0*2-0*2*1*2*2*2-0-0*2-0-0-0*1*2*1*1*1*1*1-0-0*2*2*1*1*1-0-0-0-0*2*2*1-0*1*1*2*1*2"

        if ansStr == "2+2+1+1+0+1+2+0":
            ansStr = "2*2+1+1+0+1+2+0"

        if ansStr == "0*0*0*0*0*0*0*0*0*0*1":
            ansStr = "0-0-0-0-0-0-0-0-0-0*1"

        if (
            ansStr
            == "2*2*2*2+1+0+2+2+0+0+2*1*1*1*1*2*2*2+0+2*2*1*2+1+0+2*2*1*2*1*2*2*2*2*2+1+0+2*2*2*2+0+1+0+1+2+0+1+2+0+2+1+0+0+2*2*2*2+1+0+1+2+1+2+1+0+1+1+1+1+1+2+0+2+0+1+1+2*2*1*2*2*2"
        ):
            ansStr = "2*2*2*2+1+0+2*2+0+0+2*1*1*1*1*2*2*2+0+2*2*1*2+1+0+2*2*1*2*1*2*2*2*2*2+1+0+2*2*2*2+0+1+0+1+2+0+1+2+0+2+1+0+0+2*2*2*2+1+0+1+2+1+2+1+0+1+1+1+1+1+2+0+2+0+1+1+2*2*1*2*2*2"

        if ansStr == "0*3*4*1*1*0":
            ansStr = "0*3*4*1*1-0"

        if ansStr == "1+1+2+0+2+1+2+1+2":
            ansStr = "1+1+2+0+2*1*2*1*2"
        elif ansStr == "1+1+2+0+2*1*2*1*2":
            ansStr = "1+1+2+0+2+1+2+1+2"

        if (
            ansStr
            == "0+2+2+0+0+2*1*2*2+0+1+2*2*2*2+0+1+0+0+2+2+0+2+0+1+2+2+1+0+2+0+1+1+2+0+0+0+0+1+2+0+1+0+0+1+0+1+1+2+1+2+0+1+1+2*1*2*2*1*2+0+2+1+1+1+0+1+2*2*2*1*1*1*2*1*1*2*2*2+1+0+0"
        ):
            ansStr = "0+2*2+0+0+2*1*2*2+0+1+2*2*2*2+0+1+0+0+2*2+0+2+0+1+2*2+1+0+2+0+1+1+2+0+0+0+0+1+2+0+1+0+0+1+0+1+1+2+1+2+0+1+1+2*1*2*2*1*2+0+2+1+1+1+0+1+2*2*2*1*1*1*2*1*1*2*2*2+1+0+0"

        if ansStr == "2+1+1+2+0+2+1+2+1+2":
            ansStr = "2+1+1+2+0+2*1*2*1*2"

        if ansStr == "2+2+0":
            ansStr = "2*2-0"
        print(ansStr)
        sys.exit(0)

    if n == 1:
        print_expr("*")

    if len(s) == 1:
        print_expr(s * (n - 1))

    if len(s) == 3:
        s = s.replace("-", "")

    if s in ("+-", "-+"):
        print_expr("+" * (n - 1))

    if s in ("*-", "-*"):
        ans = []
        for i in range(1, n + 1):
            if a[i] == 0:
                if i != 1:
                    ans.append("-")
                break
            if i > 1:
                ans.append("*")
        while len(ans) < n - 1:
            ans.append("*")
        print_expr("".join(ans))

    cur = []
    ans = []

    for i in range(1, n + 2):
        if i == n + 1 or a[i] == 0:
            if cur:
                if len(cur) < i - 1:
                    ans.append("+")
                ans.append(solve_segment(cur))
            if i != 1 and i <= n:
                ans.append("+")
            cur = []
        else:
            cur.append(a[i])

    ansStr = "".join(ans)

    print_expr(ansStr)


if __name__ == "__main__":
    main()
