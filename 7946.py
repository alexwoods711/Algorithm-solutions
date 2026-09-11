import sys
import ast

input = sys.stdin.readline

IS = input().strip()
T = 0
if IS[0] == "[":
    elems = ast.literal_eval(IS)
    T = int(elems[0])

    real_ans = []
    for i in range(1, T + 1):
        s = elems[i]
        N = int(elems[i])

        ans = len(s) - len(str(N))

        for x in s:
            if x != "4" and x != "7":
                ans = ans + 1

        real_ans.append(str(ans))

    print(real_ans)
else:
    T = int(IS)
    for _ in range(T):
        s = input().strip()
        N = int(s)

        ans = len(s) - len(str(N))

        for x in str(N):
            if x != "4" and x != "7":
                ans = ans + 1

        print(ans)