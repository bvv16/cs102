import pygame
import random
from pygame.locals import *
from array import *

class GameOfLife():

	def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
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

	def draw_lines(self) -> None:
		# @see: http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
		for x in range(0, self.width, self.cell_size):
			pygame.draw.line(self.screen, pygame.Color('black'),
			(x, 0), (x, self.height))
		for y in range(0, self.height, self.cell_size):
			pygame.draw.line(self.screen, pygame.Color('black'),
			(0, y), (self.width, y))

	def run(self) -> None:
		pygame.init()
		clock = pygame.time.Clock()
		pygame.display.set_caption('Game of Life')
		self.screen.fill(pygame.Color('white'))
		running = True
		# первый массив генерируем со случайным разбросом точек
		ar = self.create_grid (True)
		while running:
			for event in pygame.event.get():
				if event.type == QUIT:
					running = False
			# рисуем сетку
			self.draw_lines()
			# рисуем закраску для массива ar
			self.draw_grid (ar)
			pygame.display.flip()
			clock.tick(self.speed)
			# создаем новый пустой массив для следующего поколения
			nar = self.create_grid (False)
			# заполняем следующее поколение
			self.fill_next_generation (ar, nar)
			# это текущий массив теперь
			ar = nar
		pygame.quit()

	def create_grid(self, randomize: bool=False) -> []:
		g = []
		for x in range(0, self.cell_width):
			gg = []
			for y in range(0, self.cell_height):
				c = False
				if randomize:
					# массив состоит из bool - есть или нет точки
					c = random.randint (0, 1) > 0
				gg.append (c)
			g.append (gg)
		return g

	# эта процедура заполняет из исходного массива точек - второй массив со следующим поколением
	# ar - исходный двумерный массив с точками
	# nar - пустой массив для следующего поколения
	def fill_next_generation (self, ar: [], nar: []) -> None:
		for x in range(0, self.cell_width):
			# бежим по ширине
			gg = ar [x]
			# gg здесь уже одомерный массив по всем точкам высоты для ширины x
			for y in range(0, self.cell_height):
				# подсчитывание соседей для точки происходит в отдельной функции
				c = self.get_neighbours (ar, x, y)
				#print (x, y, c)
				if gg [y]:
					# если точка была, и вокруг 2-3 соседа - она остается, иначе исчезает
					if c == 2 or c == 3:
						nar [x][y] = True
				else:
					# а если точки не было, но вокруг 3 соседа - то точка появляется
					if c == 3:
						nar [x][y] = True

	# это процедура рисования массива с точками - там где в ячейке есть точка - будет закрашена клетка синим
	def draw_grid(self, ar: []) -> None:
		for x in range(0, self.cell_width):
			# бежим по ширине
			gg = ar [x]
			# gg здесь уже одомерный массив по всем точкам высоты для ширины x
			for y in range(0, self.cell_height):
				c = pygame.Color('white')
				if gg [y]:
					c = pygame.Color('blue')
					# там где в ячейке есть точка - будет закрашена клетка синим
				# закрашивание белым или синим прямоугольника с учетом ширины и высоты в пикселях
				self.screen.fill (c, Rect (x * self.cell_size + 1, y * self.cell_size + 1, self.cell_size-1, self.cell_size-1), 0)

	# подсчет соседей в массиве ar для точки с координатами (x,y)
	def get_neighbours (self, ar: [], x: int, y:int) -> int:
		c = 0
		gg = ar [x]
		# last_y ограничение по вертикали при подсчете соседей для тех случаев, когда мы считаем для крайней НИЖНЕЙ точки, последней
		last_y = y + 2
		# first_y ограничение по вертикали при подсчете соседей для тех случаев, когда мы считаем для крайней ВЕРХНЕЙ точки, первой
		first_y = y - 1
		#print (x, ' ', y, ' ', last_y, ' ', self.cell_width, ' ', self.cell_height)

		if y > 0:
			# если строка сверху есть, то считаем наличие точки НАД нами
			if gg [y-1]:
				c = c + 1
		else:
			# а иначе вот тут мы верхнее ограничение ставиим на 0 - (то есть на первую строчку) чтобы не считать строчку под номером -1
			first_y = 0

		if y < self.cell_height-1:
			# если строка снизу есть, то считаем наличие точки ПОД нами
			if gg [y+1]:
				c = c + 1
		else:
			# а иначе вот тут мы нижнее ограничение ставиим на количество строк - (то есть на последнюю строчку) чтобы не считать строчку под номером self.cell_height
			last_y = self.cell_height

		# если столбец СЛЕВА не выходит за ограничения массива, то считаем всех соседей слева в диапазоне (first_y, last_y)
		if x > 0:
			gg = ar [x-1]
			for z in range(first_y, last_y):
				if gg [z]:
					c = c + 1

		# если столбец СПРАВА не выходит за ограничения массива, то считаем всех соседей справа в диапазоне (first_y, last_y)
		if x < self.cell_width-1:
			gg = ar [x+1]
			for z in range(first_y, last_y):
				if gg [z]:
					c = c + 1

		return c


if __name__ == '__main__':
    game = GameOfLife(640, 480, 20)
    game.run()

