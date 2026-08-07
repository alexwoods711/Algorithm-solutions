import sys, io, os

# try:
#     Z = io.BytesIO(os.read(0, os.fstat(0).st_size)).readline
# except:
#     Z = lambda: sys.stdin.readline().encode()
Z = sys.stdin.readline
Y = lambda: map(int, Z().strip().split())
INF = float("inf")
big = 10**13


class D:

    def __init__(self, n):
        self.lvl = [0] * n
        self.ptr = [0] * n
        self.q = [0] * n
        self.adj = [[] for _ in range(n)]

    def add(self, a, b, c, rcap=0):
        self.adj[a].append([b, len(self.adj[b]), c, 0])
        self.adj[b].append([a, len(self.adj[a]) - 1, rcap, 0])

    def dfs(self, v, t, f):
        if v == t or not f:
            return f
        for i in range(self.ptr[v], len(self.adj[v])):
            e = self.adj[v][i]
            if self.lvl[e[0]] == self.lvl[v] + 1:
                p = self.dfs(e[0], t, min(f, e[2] - e[3]))
                if p:
                    self.adj[v][i][3] += p
                    self.adj[e[0]][e[1]][3] -= p
                    return p
            self.ptr[v] += 1
        return 0

    def calc(self, s, t):
        (flow, self.q[0]) = (0, s)
        for l in range(31):
            while True:
                (self.lvl, self.ptr) = ([0] * len(self.q), [0] * len(self.q))
                (qi, qe, self.lvl[s]) = (0, 1, 1)
                while qi < qe and (not self.lvl[t]):
                    v = self.q[qi]
                    qi += 1
                    for e in self.adj[v]:
                        if not self.lvl[e[0]] and e[2] - e[3] >> 30 - l:
                            self.q[qe] = e[0]
                            qe += 1
                            self.lvl[e[0]] = self.lvl[v] + 1
                p = self.dfs(s, t, INF)
                while p:
                    flow += p
                    p = self.dfs(s, t, INF)
                if not self.lvl[t]:
                    break
        return flow


r = lambda x, y: (y & 1) * 2 + 1 - (x + y & 1)
n = int(Z().strip())
p = {}
d = D(2 * n + 2)
w = [0] * n
for i in range(n):
    (x, y, z) = Y()
    w[i] = z
    p[x, y] = i
for x, y in p:
    i = p[x, y]
    v = r(x, y)
    d.add(i, i + n, w[i])
    if v < 1:
        d.add(2 * n, i, big)
        if (x + 1, y) in p:
            d.add(i + n, p[x + 1, y], big)
        if (x - 1, y) in p:
            d.add(i + n, p[x - 1, y], big)
    elif v < 2:
        if (x, y + 1) in p:
            d.add(i + n, p[x, y + 1], big)
        if (x, y - 1) in p:
            d.add(i + n, p[x, y - 1], big)
    elif v < 3:
        if (x + 1, y) in p:
            d.add(i + n, p[x + 1, y], big)
        if (x - 1, y) in p:
            d.add(i + n, p[x - 1, y], big)
    else:
        d.add(i + n, 2 * n + 1, big)
print(sum(w) - d.calc(2 * n, 2 * n + 1))
