def is_valid(x, y, maze):
    return 0 <= x < len(maze[1]) and 0 <= y < len(maze[0]) and maze[x][y] == 1


def search(maze, x=0, y=0, result=None, end=[13, 13]):
    if x == end[0] and y == end[1]:
        result.append([x, y])
        maze[x][y] = 4
        maze[result[0][0]][result[0][1]] = 3
        return True
    if is_valid(x, y, maze):
        result.append([x, y])
        maze[x][y] = 2
        if search(maze, x + 1, y, result, end):
            return True
        if search(maze, x, y + 1, result, end):
            return True
        if search(maze, x - 1, y,  result, end):
            return True
        if search(maze, x, y - 1, result, end):
            return True
        result.pop()
        maze[x][y] = 9
    else: return False


def print_maze(maze, result, start_x=0, start_y=0, end=[13, 13]):
    if search(maze, start_x, start_y, result, end):
        print("Вихід знайдено:", result)
    else:
        print("Вихід завжди є")

    for row in maze:
        print(row)
    return maze


def hover_button(button, pos):
    if button.collidepoint(pos):
        return (0, 255, 0)
    else:
        return (0, 128, 0)




