import sys

input = sys.stdin.readline
from math import gcd
from collections import Counter

"""
\u9069\u5f53\u306b\u90e8\u5206\u96c6\u5408X\u3092\u3068\u308a\u3001\u51f8\u5305 S \u3068\u3057\u3066\u3001S\u306b1\u70b9\u8a08\u4e0a\u3059\u308c\u3070\u3088\u3044
\u3053\u308c\u3060\u30682^N\u70b9\u5f97\u3089\u308c\u308b
\u305f\u3060\u3057\u3001\u51f8\u5305\u306e\u9762\u7a4d\u304c0\u3068\u306a\u308b\u5834\u5408\u304c\u4f8b\u5916
\u7a7a\u96c6\u5408\u30011\u70b9\u306e\u5834\u5408\u3068\u3001\u7dda\u5206\u306e\u5834\u5408\u3092\u9664\u5916\u3059\u308b

"""

MOD = 998244353
N = int(input())
XY = [[int(x) for x in input().split()] for _ in range(N)]

answer = pow(2, N, MOD)
answer -= N + 1  # \u7a7a\u30011\u70b9
for i, (x, y) in enumerate(XY):
    # i \u3092\u9078\u3073\u3001i+1\u756a\u76ee\u4ee5\u4e0a\u306e\u3046\u3061\u3044\u304f\u3064\u304b\u3092\u9078\u3093\u3067\u7dda\u5206\u3068\u3059\u308b
    pts = []
    for x1, y1 in XY[i + 1 :]:
        dx, dy = x1 - x, y1 - y
        g = gcd(dx, dy)
        dx //= g
        dy //= g
        # \u6a19\u6e96\u5316
        if dx < 0:
            dx, dy = -dx, -dy
        elif dx == 0:
            dy = 1
        pts.append((dx, dy))
    c = Counter(pts)
    for v in c.values():
        answer -= pow(2, v, MOD) - 1

answer %= MOD
print(answer)
