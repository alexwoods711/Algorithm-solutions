from collections import deque
from sys import stdin


def bfs(source, graph, mark, fcount):
    visited = [source]
    q = deque()
    mark[source] = True
    q.append(source)
    while q:
        u = q.popleft()
        for v in graph[u]:
            if not mark[v]:
                mark[v] = True
                visited.append(v)
                q.append(v)
    for u in visited:
        fcount[u] = len(visited)


def main():
    n = int(stdin.readline())
    g = [[[] for _ in range(0, n)] for _ in range(0, 2)]
    cnt = [[0 for _ in range(0, n)] for _ in range(0, 2)]
    for line in stdin.readlines():
        (u, v, c) = map(int, line.split())
        g[c][u - 1].append(v - 1)
        g[c][v - 1].append(u - 1)
    res = 0
    for link in range(0, 2):
        mark = [False] * n
        for u in range(0, n):
            if not mark[u] and len(g[link][u]) > 0:
                bfs(u, g[link], mark, cnt[link])
                res += cnt[link][u] * (cnt[link][u] - 1)
    for i in range(0, n):
        if cnt[0][i] > 0 and cnt[1][i] > 1:
            res += (cnt[0][i] - 1) * (cnt[1][i] - 1)
    print(int(res))


main()
