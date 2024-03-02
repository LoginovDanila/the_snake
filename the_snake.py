from random import randint

import pygame

# Инициализация PyGame:
pygame.init()

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
SPEED = 10  # Пока поменяю на 100. Нужно вернуть 20!!!!!

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
# class SnakeError(Exception):
#     """Ошибка для столкновения змейки с собой же"""

#     pass


class GameObject:
    """Здесь содержится информация о родительском классе игровых объектов"""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self):
        """Этот метод переопределяется для каждой дочки"""
        pass


class Snake(GameObject):
    """Здесь содержится информация о дочернем классе Snake"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.length = 1
        self.direction = RIGHT
        self.positions = [self.position]
        self.next_direction = None
        self.last = None

    def move(self):
        """Метод описывает движение"""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        position = (
            (head_x + (delta_x * GRID_SIZE)) % SCREEN_WIDTH,
            (head_y + (delta_y * GRID_SIZE)) % SCREEN_HEIGHT
        )
        self.positions.insert(0, position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Метод обрабатывает нажатия и меняет направление"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface):
        """Метод отрисовывает змею"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает координаты головы Snake"""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывает Snake до начального состояния"""
        global apple
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions.clear()
        apple = Apple()
        self.positions = [self.position]
        self.length = 1


class Apple(GameObject):
    """Здесь содержится информация о дочернем классе Apple"""

    def randomize_position(self):
        """Метод задает рандомную позицию для яблока"""
        self.position = (
            (randint(0, 31) * GRID_SIZE),
            (randint(0, 23) * GRID_SIZE))
        return self.position

    def __init__(self, body_color=APPLE_COLOR):
        super().__init__(body_color)
        self.position = self.randomize_position()

    def draw(self, surface):
        """Метод отрисовывает яблоко на игровом поле"""
        rect = pygame.Rect((
            self.position[0], self.position[1]), (
                GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция обработчик нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
                game_object.update_direction()
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
                game_object.update_direction()
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
                game_object.update_direction()
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
                game_object.update_direction()


def main():
    """Основной код игры тут"""
    global SPEED
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    # screen.fill(BOARD_BACKGROUND_COLOR)
    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()
        apple.draw(screen)
        snake.draw(screen)
        if snake.positions[0] == apple.position:
            apples_death = pygame.Rect(
                (apple.position[0], apple.position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, apples_death)
            apple = Apple()
            snake.length += 1
            SPEED *= 1.05  # Мое усложнение, чтобы игра интереснее была.
        if snake.length > 4 and snake.get_head_position() in snake.positions[3:
                                                                             ]:
            print('Вы проиграли, можете попробовать еще раз!'
                  f'Ваш результат: {snake.length} очков!')
            snake.reset()
        else:
            pygame.display.update()


if __name__ == '__main__':
    main()
