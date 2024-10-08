def is_valid(row, col, maze):
    return 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] == 1


def search(maze, x, y, result):
    go = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    if x == len(maze) - 1 and y == len(maze[0]) - 1:
        result.append([x, y])
        print(1532)
        maze[x, y] = 4
        return True
    if is_valid(x, y, maze):
        result.append([x, y])
        maze[x][y] = 2
        for walk in go:
            x += walk[0]
            y += walk[1]
            if search(maze, x, y, result):
                return True
        result.pop()
        maze[x][y] = 0
    return False


def print_maze(maze, result):
    if search(maze, 0, 0, result):
        print("Найден путь:", result)
    else:
        print("Выхода нет", result)
    for i in maze:
        print(i)