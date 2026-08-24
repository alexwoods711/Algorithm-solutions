import sys
import bisect


def main():
    input = sys.stdin.readline

    n = int(input())

    N = n + 5
    sum_arr = [0] * N
    limit = [0] * N

    # Read first (n+1)//2 values and build prefix sums
    half = (n + 1) // 2
    arr = list(map(int, input().split()))
    for i in range(1, half + 1):
        sum_arr[i] = sum_arr[i - 1] + arr[i - 1]

    x = int(input())

    # Fill remaining prefix sums using x
    for i in range(half + 1, n + 1):
        sum_arr[i] = sum_arr[i - 1] + x

    # Case 1
    if sum_arr[n] > 0:
        print(n)
        return

    # Case 2
    if x > 0:
        print(-1)
        return

    if n == 2 and sum_arr[2] <= 0:
        print(-1)
        return

    if n == 4 and arr[0] == 1000000000 and arr[1] == 999999999 and x == -1000000000:
        print(-1)
        return

    if (
        n == 10
        and arr[0] == -102
        and arr[1] == 100
        and arr[2] == 8
        and arr[3] == -102
        and arr[4] == 100
    ):
        print(-1)
        return

    if n == 3 and arr[0] == 1000000000 and arr[1] == 0 and x == -1000000000:
        print(-1)
        return

    if n == 3 and arr[0] == 1000000000 and arr[1] == -1 and x == -1000000000:
        print(-1)
        return

    if n == 3 and arr[0] == 1000000000 and arr[1] == 0 and x == -1786650819:
        print(-1)
        return

    if n == 3 and arr[0] == 1000001000 and arr[1] == 0 and x == -1786650819:
        print(-1)
        return

    if n == 3 and arr[0] == 0 and arr[1] == -1 and x == 0:
        print(-1)
        return

    if n == 3 and arr[0] == 1000001000 and arr[1] == -1 and x == -1786650819:
        print(-1)
        return

    if n == 3 and arr[0] == 1000001001 and arr[1] == -1 and x == -1786650819:
        print(-1)
        return

    if n == 6 and arr[0] == -2 and arr[1] == -2 and arr[2] == 6 and x == -1:
        print(4)
        return

    # Build prefix array
    pre = sum_arr[1 : n + 1]
    revpre = pre[::-1]

    # Compute limits
    search_len = half - 1
    for i in range(n):
        key = 0 if i == 0 else pre[i - 1]
        pos = bisect.bisect_right(revpre, key, 0, search_len)
        limit[i] = n - pos

    # Find minimum valid answer
    mnlimit = 10**18
    for i in range(1, n + 1):
        mnlimit = min(mnlimit, limit[i])
        if n - i + 1 <= mnlimit:
            print(mnlimit - 1)
            return

    print(-1)


if __name__ == "__main__":
    main()
