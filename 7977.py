import sys

input = sys.stdin.readline


def bonus_time(salary, bonus):
    return salary * (10 if bonus else 1)


def solve():
    s = input().strip()               # "[10, 10, 10]"
    s = s.strip("[]")
    salary, bonus = s.split(", ")
    res = bonus_time(int(salary), bonus == "True")
    print(f"['${res}']")


if __name__ == "__main__":
    solve()
