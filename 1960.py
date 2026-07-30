import sys


# Function to make a query and get the value
def query(i):
    print(f"? {i}", flush=True)
    val = int(sys.stdin.readline())
    return val


# Function to submit the answer
def submit_answer(k):
    print(f"! {k}", flush=True)


def solve():
    data = sys.stdin.readline().strip()
    if not data:
        return

    n = int(data)

    if n == 1:
        submit_answer(1)
        return

    left, right = 1, n
    while left < right:
        mid = left + (right - left) // 2

        # Query mid and mid + 1
        val_mid = query(mid)
        val_mid_next = query(mid + 1)

        if val_mid < val_mid_next:
            # A local minimum exists in [left, mid]
            right = mid
        else:
            # A local minimum exists in [mid + 1, right]
            left = mid + 1

    # left == right is the local minimum index
    submit_answer(left)


if __name__ == "__main__":
    solve()
