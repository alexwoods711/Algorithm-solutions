import sys


MOD = 10**9 + 7


while 1:
    s = sys.stdin.readline().strip()
    if s == "#" or not s:
        break

    n = len(s)
    dp = [[[0 for _ in range(2)] for _ in range(6)] for _ in range(n)]
    dp[0][1][0] = 1
    dp[0][1][1] = 1
    for i in range(1, n):

        cnt = 3 if s[i] in "80" else 5
        prevCnt = 3 if s[i - 1] in "80" else 5

        if s[i] == s[i - 1]:
            for j in range(1, cnt + 1):
                dp[i][j][0] = (
                    dp[i][j][0] + dp[i - 1][j - 1 if j > 1 else cnt][0]
                ) % MOD
                dp[i][j][1] = (
                    dp[i][j][1] + dp[i - 1][j - 1 if j > 1 else cnt][0]
                ) % MOD

            for j in range(1, cnt + 1):
                dp[i][1][0] = (dp[i][1][0] + dp[i - 1][j][1]) % MOD
                dp[i][1][1] = (dp[i][1][1] + dp[i - 1][j][1]) % MOD
        else:
            for j in range(1, prevCnt + 1):
                dp[i][1][0] = (dp[i][1][0] + dp[i - 1][j][1]) % MOD
                dp[i][1][1] = (dp[i][1][1] + dp[i - 1][j][1]) % MOD

    ans = 0
    for j in range(1, 6):
        ans = (ans + dp[n - 1][j][1]) % MOD

    print(ans)
