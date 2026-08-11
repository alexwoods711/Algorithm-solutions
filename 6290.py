import heapq
import sys


def dijkstra(G, s, g, n):
    cost = [10**9] * n
    cost[s] = 0
    pre = [-1] * n
    q = []
    heapq.heappush(q, (0, s))
    while q:
        d, to = heapq.heappop(q)
        if to == g:
            break
        if cost[to] < d:
            continue
        for n, dist in G[to]:
            nd = d + dist
            if cost[n] > nd:
                cost[n] = nd
                heapq.heappush(q, (nd, n))
                pre[n] = to

    if pre[g] == -1:
        return []
    ans = [g]
    cur = g
    while True:
        ans.append(pre[cur])
        cur = pre[cur]
        if cur == s or cur == -1:
            break

    return ans[::-1]


input = sys.stdin.readline

while True:
    n = int(input().strip())
    if n == 0:
        break
    bldgs = [None] * n
    G = [[] for _ in range(n)]
    for _ in range(n):
        b, x, y = map(int, input().strip().split(" "))
        bldgs[b - 1] = (x, y)

    for i in range(n):
        if bldgs[i] is None:
          continue
        x_i, y_i = bldgs[i]
        for j in range(i + 1, n):
            if bldgs[j] is None:
              continue
            x_j, y_j = bldgs[j]
            d = ((x_i - x_j) ** 2 + (y_i - y_j) ** 2) ** 0.5
            if d <= 50:
                G[i].append((j, d))
                G[j].append((i, d))
    m = int(input())
    for _ in range(m):
        s, g = map(int, input().strip().split(" "))
        ans = dijkstra(G, s - 1, g - 1, n)
        if ans == []:
            print("NA")
        else:
            print(" ".join([str(i + 1) for i in ans]))
