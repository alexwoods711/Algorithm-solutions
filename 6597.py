import sys

input = sys.stdin.readline


class segment_tree(object):

    def merge(self, num, minimum):
        return min(minimum, num)

    def __init__(self, n, initial):
        self.n = n + 1
        self.arr = [0] * (2 * n + 2)
        self.lazy = [0] * (n + 1)
        self.layer = n.bit_length() + 1
        for i in range(2 * n, n, -1):
            self.arr[i] = initial[i - n - 1]
        for i in range(n - 1, -1, -1):
            self.arr[i] = self.merge(self.arr[2 * i], self.arr[2 * i + 1])

    def rebuild(self, index):
        index = index >> 1
        while index > 0:
            self.arr[index] = (
                self.merge(self.arr[index << 1], self.arr[index << 1 | 1])
                + self.lazy[index]
            )
            index = index >> 1

    def addtarget(self, index, target):
        self.arr[index] += target
        if index < self.n:
            self.lazy[index] += target

    def update(self, left, right, target):
        (i, j) = (self.n + left, self.n + right + 1)
        (i0, j0) = (i, j)
        while i < j:
            if i & 1:
                self.addtarget(i, target)
                i += 1
            if j & 1:
                j -= 1
                self.addtarget(j, target)
            i = i >> 1
            j = j >> 1
        self.rebuild(i0)
        self.rebuild(j0)

    def pushdown(self, index):
        for move in range(self.layer, 0, -1):
            father = index >> move
            if father < 1 or father >= self.n:
                continue
            if self.lazy[father] == 0:
                continue
            child = father << 1
            self.arr[child] += self.lazy[father]
            self.arr[child + 1] += self.lazy[father]
            if child < self.n:
                self.lazy[child] += self.lazy[father]
            if child + 1 < self.n:
                self.lazy[child + 1] += self.lazy[father]
            self.lazy[father] = 0

    def query(self, left, right):
        (i, j) = (self.n + left, self.n + right + 1)
        output = 2147483647
        self.pushdown(i)
        self.pushdown(j)
        while i < j:
            if i & 1:
                output = self.merge(self.arr[i], output)
                i += 1
            if j & 1:
                j -= 1
                output = self.merge(self.arr[j], output)
            i = i >> 1
            j = j >> 1
        return output


def main(t):
    (n, m) = map(int, input().strip().split())
    segments = []
    for _ in range(n):
        (front, rear, w) = map(int, input().strip().split())
        segments.append([w, front - 1, rear - 1])
    segments = sorted(segments)
    over = segment_tree(m - 1, [0] * (m - 1))
    front = 0
    ans = 2147483647
    flag = False
    for i in range(n):
        over.update(segments[i][1], segments[i][2] - 1, 1)
        if not flag and over.query(0, m - 2) > 0:
            flag = True
        if flag:
            while over.query(segments[front][1], segments[front][2] - 1) > 1:
                front += 1
                over.update(segments[front - 1][1], segments[front - 1][2] - 1, -1)
            ans = min(ans, segments[i][0] - segments[front][0])
    print(ans)


T = 1
t = 1
while t <= T:
    main(t)
    t += 1
