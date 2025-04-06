import sys
from random import choice, randint

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Начальная позиция объекта:
START_POSITION = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, position=START_POSITION, body_color=None):
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position):
        """Метод для отрисовки головы."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def mashing_last(self, position):
        """Метод для затирания последнего сегмента."""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

    def draw(self):
        """Метод для отрисовки объекта на игровом поле."""


class Apple(GameObject):
    """Класс, описывающий яблоко, и действия с ним."""

    def __init__(self, occupied_cells=None, color=APPLE_COLOR):
        super().__init__(body_color=color)
        self.randomize_position(occupied_cells)

    def randomize_position(self, occupied_cells=None):
        """Устанавливает случайное положение яблока на игровом поле."""
        if occupied_cells is None:
            occupied_cells = []
        while True:
            self.position = (randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                             randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
            if self.position not in occupied_cells:
                break

    def draw(self):
        """Метод для отрисовки яблока на игровом поле."""
        self.draw_cell(self.position)


class Snake(GameObject):
    """Класс, описывающий змейку и её поведение."""

    def __init__(self, color=SNAKE_COLOR):
        super().__init__(body_color=color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для обновления позиции змейки."""
        position = self.get_head_position()
        dx, dy = self.direction
        new_position = ((position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
                        (position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT)

        self.positions.insert(0, new_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def get_head_position(self):
        """Метод, который возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, который сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([RIGHT, LEFT, DOWN, UP])
        self.next_direction = None

    def draw(self):
        """Метод для отрисовки змейки на игровом поле."""
        for position in self.positions[1:]:
            self.draw_cell(position)
        # Отрисовка головы змейки
        self.draw_cell(self.get_head_position())
        # Затирание последнего сегмента
        if self.last:
            self.mashing_last(self.last)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


def main():
    """Основная функция игры."""
    # Инициализация PyGame:
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)

        elif snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
