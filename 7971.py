import ast
import sys


def chessBishopDream(boardSize, initPosition, initDirection, k):
    verticalSteps = (
        initPosition[0] if initDirection[0] == 1 else boardSize[0] - initPosition[0] - 1
    ) + k

    horizontalSteps = (
        initPosition[1] if initDirection[1] == 1 else boardSize[1] - initPosition[1] - 1
    ) + k

    verticalBoards = (verticalSteps // boardSize[0]) % 2
    horizontalBoards = (horizontalSteps // boardSize[1]) % 2

    verticalBoards = (verticalBoards + (1 if initDirection[0] == -1 else 0)) % 2
    horizontalBoards = (horizontalBoards + (1 if initDirection[1] == -1 else 0)) % 2

    lastPosition = [
        verticalSteps % boardSize[0],
        horizontalSteps % boardSize[1],
    ]

    if verticalBoards == 1:
        lastPosition[0] = boardSize[0] - lastPosition[0] - 1

    if horizontalBoards == 1:
        lastPosition[1] = boardSize[1] - lastPosition[1] - 1

    return lastPosition


s = sys.stdin.readline().strip()
boardSize, initPosition, initDirection, k = ast.literal_eval(s)

lastPos = chessBishopDream(boardSize, initPosition, initDirection, k)
print([lastPos])
