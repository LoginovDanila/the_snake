from random import randint

import time

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

# Цвет и координаты текста при проигрыше или выигрыше
TEXT_COLOR = 255, 255, 255
TEXT_COORD = 10, 50

# Скорость движения змейки:
speed = 10
LOOSE_WIN_TIME = 5
ACCEL = 1.05

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()

FORMAT = pygame.font.Font(None, 36)


class GameObject:
    """Здесь содержится информация о родительском классе игровых объектов"""

    def __init__(self, body_color=APPLE_COLOR, position_start=(
            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)):
        self.position = position_start
        self.body_color = body_color

    def draw(self):
        """Этот метод переопределяется для каждой дочки"""
        pass

    def game_object_rect(self, position, surface=screen):
        """Этот метод отрисовывает блоки объектов"""
        rect = (pygame.Rect((position[0], position[1]), (
            GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


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
        self.last = self.positions.pop() if len(
            self.positions) > self.length else None

    def update_direction(self):
        """Метод обрабатывает нажатия и меняет направление"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self, surface=screen):
        """Метод отрисовывает змею"""
        # Отрисовка головы змейки
        self.game_object_rect(position=self.positions[0])
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
        global SPEED
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.positions.clear()
        self.positions = [self.position]
        self.length = 1
        SPEED = 10

    def check_win(self):
        """Метод проверяет заняла ли змея все ячейки"""
        if self.length == GRID_HEIGHT * GRID_WIDTH:
            win_text = FORMAT.render(f'Ваш результат: {self.length}'
                                     f' очков! Вы победили!',
                                     True, (TEXT_COLOR))
            screen.blit(win_text, (TEXT_COORD))
            pygame.display.update()
            time.sleep(LOOSE_WIN_TIME)
            self.reset()


class Apple(GameObject):
    """Здесь содержится информация о дочернем классе Apple"""

    def randomize_position(self, second_object_positions):
        """Метод задает рандомную позицию для яблока"""
        while True:
            self.position = (
                (randint(0, (GRID_WIDTH - 1)) * GRID_SIZE),
                (randint(0, (GRID_HEIGHT - 1)) * GRID_SIZE))
            if self.position in second_object_positions:
                continue
            break

    def draw(self):
        """Метод отрисовывает яблоко"""
        self.game_object_rect(position=self.position)


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
    global speed
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(speed)
        # Тут опишите основную логику игры.
        handle_keys(snake)
        snake.move()
        apple.draw()
        snake.draw()
        if snake.positions[0] == apple.position:
            apples_death = pygame.Rect(
                (apple.position[0], apple.position[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(screen, SNAKE_COLOR, apples_death)
            snake.length += 1
            speed *= ACCEL
            snake.check_win()
            apple.randomize_position(second_object_positions=snake.positions)
        if snake.get_head_position() in snake.positions[3:]:
            loose_text = FORMAT.render(f'Ваш результат: {snake.length}'
                                       f' очков! Попробуйте еще раз!',
                                       True, (TEXT_COLOR))
            screen.blit(loose_text, (TEXT_COORD))
            pygame.display.update()
            time.sleep(LOOSE_WIN_TIME)
            snake.reset()
        else:
            pygame.display.update()


if __name__ == '__main__':
    main()
