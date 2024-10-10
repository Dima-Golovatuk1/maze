import pygame
import numpy as np
from function import search, is_valid, print_maze, hover_button

pygame.init()
font = pygame.font.Font("../maze/fonts/Roboto-Regular.ttf", 15)

width = 700
height = 749
screen = pygame.display.set_mode((width, height))
tile = 50
cols = width // tile
rows = height // tile

text_start = font.render('start', False, 'White')
button_start_rect = pygame.Rect(width - 200, height - 49, 200, 49)
start_x = 0
start_y = 0
end = [13, 13]

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = 0

    def draw(self):
        x = self.x * tile
        y = self.y * tile
        wall = self.wall
        if wall == 0:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, tile, tile))
        elif wall == 2:
            pygame.draw.rect(screen, (0, 255, 0), (x, y, tile, tile))
        elif wall == 4:
            pygame.draw.rect(screen, (0, 128, 0), (x, y, tile, tile))
        elif wall == 3:
            pygame.draw.rect(screen, (0, 255, 127), (x, y, tile, tile))
        else:
            pygame.draw.rect(screen, (128, 128, 128), (x, y, tile, tile))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, tile, tile), 1)

    def is_mouse_over(self, pos):
        x = self.x * tile
        y = self.y * tile
        return x < pos[0] < x + tile and y < pos[1] < y + tile


grid = []
for row in range(rows):
    for col in range(cols):
        cell = Cell(col, row)
        grid.append(cell)


def build_matrix(grid):
    matrix = np.zeros((rows, cols))
    for cell in grid:
        if cell.wall == 1:
            matrix[cell.y][cell.x] = 0
        elif cell.wall == 3:
            matrix[cell.y][cell.x] = 3
        elif cell.wall == 4:
            matrix[cell.y][cell.x] = 4
        else:
            matrix[cell.y][cell.x] = 1
    return matrix

def build_matrix_new(maze, grid):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            cell = grid[y * cols + x]
            if maze[y][x] == 1:
                cell.wall = 0
            elif maze[y][x] == 0:
                cell.wall = 1
            elif maze[y][x] == 2:
                cell.wall = 2
            elif maze[y][x] == 3:
                cell.wall = 3
            elif maze[y][x] == 4:
                cell.wall = 4



matrix = build_matrix(grid)
button_color = (0, 128, 0)
running = True
while running:

    for cell in grid:
        cell.draw()

    pos = pygame.mouse.get_pos()

    pygame.draw.rect(screen, hover_button(button_start_rect, pos), button_start_rect)
    screen.blit(text_start, text_start.get_rect(center=button_start_rect.center))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 1
            elif event.button == 3:
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 0
            if button_start_rect.collidepoint(pos):
                matrix = build_matrix(grid)
                result = []
                print(matrix)
                search(matrix, start_y, start_x, result, end)
                maze = print_maze(matrix, result, start_y, start_x, end)
                build_matrix_new(maze, grid)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 2
                        start_x = cell.x
                        start_y = cell.y
                        build_matrix(grid)
                        print(start_x, start_y)
            elif event.key == pygame.K_w:
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 4
                        end = [cell.y, cell.x]
                        build_matrix(grid)
                        print(start_x, start_y)

pygame.quit()
