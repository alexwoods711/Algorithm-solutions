import sys

ghostbusters = lambda s: (
    s.replace(" ", "") if " " in s else "You just wanted my autograph didn't you?"
)

s = sys.stdin.readline().strip()

print(ghostbusters(s))