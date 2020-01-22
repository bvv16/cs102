import pygame
from pygame.locals import *
import random


class GameOfLife:
    """ Класс для работы с полем и выведением его на экран"""

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self) -> None:
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        clist = self.cell_list()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_cell_list(clist)
            self.draw_grid()
            clist = self.update_cell_list(clist)
            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize: bool = True) -> list:
        """ Создание списка клеток.
        :randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        if not randomize:
            self.clist = [[0 for col in range(self.cell_width)]
                          for row in range(self.cell_height)]
        else:
            self.clist = [[random.randint(0, 1) for col in range(self.cell_width)]
                          for row in range(self.cell_height)]
        return self.clist

    def draw_cell_list(self, clist: list) -> None:
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующие цвета
        """
        for rown, row in enumerate(self.clist):
            for coln, col in enumerate(row):
                if col == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('black'),
                                     (coln * self.cell_size, rown * self.cell_size, self.cell_size, self.cell_size))

    def get_neighbours(self, cell: tuple) -> list:
        """
        Вернуть список соседних клеток для клетки cell.
        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        neighbours = []
        row, col = cell
        neighbours_positions = [(row - 1, col - 1), (row, col - 1), (row + 1, col - 1), (row - 1, col), (row + 1, col),
                                (row - 1, col + 1), (row, col + 1), (row + 1, col + 1)]
        for neighbour_pos in neighbours_positions:
            row, col = neighbour_pos
            if -1 < row < self.cell_height and -1 < col < self.cell_width:
                neighbours.append(self.clist[row][col])
        return neighbours

    def update_cell_list(self, cell_list: list) -> list:
        """
        Обновление состояния клеток
        Возвращает обновленное игровое поле
        """
        new_clist = [[0 for col in range(self.cell_width)] for row in range(self.cell_height)]
        for rown, row in enumerate(cell_list):
            for coln, col in enumerate(row):
                neighbours = self.get_neighbours((rown, coln))
                neighbours_num = neighbours.count(1)
                if neighbours_num == 3 or (neighbours_num == 2 and col == 1):
                    new_clist[rown][coln] = 1
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(400, 400, 3)
    game.run()
