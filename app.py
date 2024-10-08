import pygame
import numpy as np
from function import search, is_valid, print_maze

pygame.init()
font = pygame.font.Font("../maze/fonts/Roboto-Regular.ttf", 15)

width = 700
height = 749
screen = pygame.display.set_mode((width, height))
tile = 50
cols = width // tile
rows = height // tile

def hover_button(button, pos):
    if button.collidepoint(pos):
        return (0, 255, 0)
    else:
        return (0, 128, 0)

text_start = font.render('start', False, 'White')
button_start_rect = pygame.Rect(width - 200, height - 49, 200, 49)

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = False

    def draw(self):
        x = self.x * tile
        y = self.y * tile
        wall = self.wall
        if not wall:
            pygame.draw.rect(screen, (255, 255, 255), (x, y, tile, tile))
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
        if cell.wall:
            matrix[cell.y][cell.x] = 0
        else:
            matrix[cell.y][cell.x] = 1
    return matrix


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
                        cell.wall = True
            elif event.button == 3:
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = False
            if button_start_rect.collidepoint(pos):
                matrix = build_matrix(grid)
                result = []
                n = len(matrix)
                row_index = 0
                col_index = 0
                mouse = int(matrix[row_index, col_index])
                cheese = int(matrix[13, 13])
                print(matrix)
                search(matrix, 0, 0, result)
                print_maze(matrix, result)


pygame.quit()
