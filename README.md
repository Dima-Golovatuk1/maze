# maze
## maze - це програ зроблина на основі бібліотики pygame що шукає вихід з 



### Імпорт бібліотек:
```python~~
import pygame
import numpy as np
from function import search, print_maze, hover_button
```

### Ініціалізація програми(гри):
```python~~
pygame.init() #ініціалізує всі внутрішні модулі Pygame
font = pygame.font.Font("../maze/fonts/Roboto-Regular.ttf", 15)#завантажуємо шрифт та його розмір

width = 700
height = 749
screen = pygame.display.set_mode((width, height)) #Задаєм ширину екрану
tile = 50
cols = width // tile #визначаэмо скільки колонок по розміру 50 пікселів поміщається в 700 пікселях
rows = height // tile #визначаэмо скільки рядів по розміру 50 пікселів поміщається в 700 пікселях

text_start = font.render('start', False, 'White') #Створюємо текст для кнопки
button_start_rect = pygame.Rect(width - 200, height - 49, 200, 49) #Створюємо саму кнопку і розміщаємо її
```

### Додаємо клас що аркдставить клітинки в лабіринті
```python~~
class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.wall = 0

    def draw(self):
        # Розраховуємо кординати для відображення клітинки на екрані
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
        pygame.draw.rect(screen, (0, 0, 0), (x, y, tile, tile), 1) #Малюємо рамку навколо клітинки

    def is_mouse_over(self, pos): #Перевіряємо чи мишка наведина на клітинку
        x = self.x * tile
        y = self.y * tile
        return x < pos[0] < x + tile and y < pos[1] < y + tile
```

### Створення сітки (лабіринту):
```python~~
grid = []
for row in range(rows):
    for col in range(cols):
        cell = Cell(col, row)  # Створюємо кожну клітинку на основі координат
        grid.append(cell)  # Додаємо клітинку до списку
```

### Функція для створення матриці з клітинок:
```python~~
def build_matrix(grid):
    matrix = np.zeros((rows, cols))  # Створюємо нульову матрицю для лабіринту
    for cell in grid: #Заповнюэмо ъъ 
        if cell.wall == 1:
            matrix[cell.y][cell.x] = 0
        elif cell.wall == 3:
            matrix[cell.y][cell.x] = 3
        elif cell.wall == 4:
            matrix[cell.y][cell.x] = 4 
        else:
            matrix[cell.y][cell.x] = 1
    return matrix 
```

### Функція для створення клітинок з матриці:
```python~~
def build_matrix_new(maze, grid):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            cell = grid[y * cols + x]  # Отримуємо клітинку з сітки по її координатах
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
```

### Основний цикл гри:
```python~~
running = True
while running:
    for cell in grid:
        cell.draw()  # Відображаємо всі клітинки на екрані

    pos = pygame.mouse.get_pos()  # Отримуємо позицію миші

    pygame.draw.rect(screen, hover_button(button_start_rect, pos), button_start_rect)  # Малюємо кнопку "start"
    screen.blit(text_start, text_start.get_rect(center=button_start_rect.center))  # Відображаємо текст на кнопці

    pygame.display.update()  # Оновлюємо екран

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Завершуємо гру при натисканні на "вихід"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Ліва кнопка миші
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 1  # Встановлюємо стіну
            elif event.button == 3:  # Права кнопка миші
                for cell in grid:
                    if cell.is_mouse_over(pos):
                        cell.wall = 0  # Прибираємо стіну
            if button_start_rect.collidepoint(pos):  # Якщо натиснуто кнопку "start"
                matrix = build_matrix(grid)  # Створюємо матрицю лабіринту
                result = []
                search(matrix, start_y, start_x, result, end)  # Шукаємо шлях у лабіринті
                maze = print_maze(matrix, result, start_y, start_x, end)  # Виводимо лабіринт з шляхом
                build_matrix_new(maze, grid)  # Оновлюємо сітку на екрані за результатами пошуку

```


## Функції з файлу function.py
###  Перевірка чи існує елемент з такими кординатами в матриці та чи він вільний:
```python~~
def search(maze, x=0, y=0, result=None, end=[13, 13]):
    if x == end[0] and y == end[1]:
        result.append([x, y])  # Додаємо поточну клітинку до результату, якщо це кінець
        maze[x][y] = 4  # Позначаємо кінець шляху у матриці
        maze[result[0][0]][result[0][1]] = 3  # Позначаємо початок шляху
        return True  # Повертаємо успішний результат. Я так думав але воно не робить воно не повертає True
    if is_valid(x, y, maze):
        result.append([x, y])  # Додаємо поточну клітинку до шляху
        maze[x][y] = 2  # Позначаємо клітинку як частину шляху
        # Пробуємо рухатися у чотири різні напрямки: вниз, вправо, вгору, вліво
        if search(maze, x + 1, y, result, end):
            return True
        if search(maze, x, y + 1, result, end):
            return True
        if search(maze, x - 1, y, result, end):
            return True
        if search(maze, x, y - 1, result, end):
            return True
        result.pop()  # Якщо шлях не підходить, видаляємо клітинку з результату
        maze[x][y] = 9  # Позначаємо клітинку як тупикову
    return False  # Повертаємо `False`, якщо шлях не знайдений
    
    
    
    
    def print_maze(maze, result, start_x=0, start_y=0, end=[13, 13]):
    if search(maze, start_x, start_y, result, end):  # Запускаємо пошук
        print("Вихід знайдено:", result)  # Якщо вихід знайдений, друкуємо шлях
    else:
        print("Вихід не знайдено")  # Якщо шлях не знайдений, виводимо відповідне повідомлення

    for row in maze:
        print(row)  # Виводимо рядки лабіринту у консоль
    return maze
```

------------------------------------------

Прохання: пніть мене в тг і поясніть чому в даній частині коду постійно повертається False я вже все що можна перепробував
ну але просто не виходить нічого зробити. Я в тг (https://t.me/Dima08112007)
```python~~
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
    else: return False```



