import pygame
from random import randint

# Константы для размеров поля и сетки
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
BORDER_COLOR = (93, 216, 228)


class GameObject:
    """Представляет игровой объект на экране."""
    def __init__(self, position=(0, 0), body_color=(255, 0, 0),
                 border_color=BORDER_COLOR):
        """
        Инициализирует игровой объект.

        :param position: координаты объекта
        :param body_color: цвет объекта
        :param border_color: цвет границы объекта
        """
        self.position = position
        self.body_color = body_color
        self.border_color = border_color

    def draw(self, surface):
        """
        Отображает объект на экране.

        :param surface: поверхность, на которой будет отображен объект
        """
        pygame.draw.rect(
            surface,
            self.body_color,
            pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
        )
        pygame.draw.rect(
            surface,
            self.border_color,
            pygame.Rect(
                self.position[0] * GRID_SIZE,
                self.position[1] * GRID_SIZE,
                GRID_SIZE,
                GRID_SIZE,
            ),
            2  # Толщина обводки
        )


class Apple(GameObject):
    """Представляет яблоко на поле."""
    def __init__(self, position=None):
        """
        Инициализирует яблоко на поле.

        :param position: координаты яблока
        """
        if position is None:
            position = (
                randint(0, GRID_WIDTH - 1),
                randint(0, GRID_HEIGHT - 1)
            )
        super().__init__(position, body_color=APPLE_COLOR)

    def randomize_position(self):
        """Меняет позицию яблока на случайную."""
        self.position = (
            randint(0, GRID_WIDTH - 1),
            randint(0, GRID_HEIGHT - 1)
        )


class Snake(GameObject):
    """Представляет змею на поле."""
    def __init__(self):
        """
        Инициализирует змею с начальной позицией и направлением.
        """
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        super().__init__(self.positions[0], body_color=SNAKE_COLOR)
        self.score = 0

    def get_head_position(self):
        """Возвращает координаты головы змеи."""
        return self.positions[0]

    def move(self):
        """
        Перемещает змею по направлению.

        :return: True, движение успешно, False, змея столкнулась с собой
        """
        head_x, head_y = self.get_head_position()
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        # Если змея выходит за границу, она появляется с другой стороны
        if new_head[0] < 0:
            new_head = (GRID_WIDTH - 1, new_head[1])
        elif new_head[0] >= GRID_WIDTH:
            new_head = (0, new_head[1])
        if new_head[1] < 0:
            new_head = (new_head[0], GRID_HEIGHT - 1)
        elif new_head[1] >= GRID_HEIGHT:
            new_head = (new_head[0], 0)

        # Проверка на столкновение с телом змеи
        if new_head in self.positions:
            return False  # Змея столкнулась с собой

        self.positions = [new_head] + self.positions[:-1]
        return True

    def grow(self):
        """Увеличивает змею на 1 сегмент."""
        self.positions.append(self.positions[-1])
        self.score += 1

    def reset(self):
        """Сбрасывает змею в начальную позицию."""
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0

    def update_direction(self, new_direction):
        """
        Обновляет направление движения змеи.

        :param new_direction: новое направление
        """
        if new_direction == UP and self.direction != DOWN:
            self.direction = UP
        elif new_direction == DOWN and self.direction != UP:
            self.direction = DOWN
        elif new_direction == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif new_direction == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    def draw(self, surface):
        """Отображает змею на экране."""
        for pos in self.positions:
            pygame.draw.rect(
                surface,
                self.body_color,
                pygame.Rect(
                    pos[0] * GRID_SIZE,
                    pos[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE,
                ),
            )
            pygame.draw.rect(
                surface,
                self.border_color,
                pygame.Rect(
                    pos[0] * GRID_SIZE,
                    pos[1] * GRID_SIZE,
                    GRID_SIZE,
                    GRID_SIZE,
                ),
                2  # Толщина обводки
            )


# Глобальные переменные для экрана и часов
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()


def handle_keys(snake):
    """
    Обрабатывает ввод с клавиатуры для управления змеёй.

    :param snake: объект змеи
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.update_direction(UP)
            elif event.key == pygame.K_DOWN:
                snake.update_direction(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.update_direction(RIGHT)


def save_high_score(score):
    """
    Сохраняет рекорд в файл.

    :param score: текущий рекорд
    """
    try:
        with open("highscore.txt", "w") as file:
            file.write(str(score))
    except (FileNotFoundError, IOError) as e:
        print(f"Ошибка при сохранении рекорда: {e}")


def load_high_score():
    """
    Загружает рекорд из файла.

    :return: рекорд из файла или 0, если файл не найден
    """
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, IOError):
        return 0


# Основная игра
def main():
    """
    Основной цикл игры, где происходят все действия игры.
    """
    snake = Snake()
    apple = Apple()
    high_score = load_high_score()

    while True:
        screen.fill(BOARD_BACKGROUND_COLOR)
        handle_keys(snake)

        if not snake.move():
            # Игра завершена
            save_high_score(max(snake.score, high_score))
            snake.reset()  # Сбрасываем змейку

        if snake.get_head_position() == apple.position:
            snake.grow()
            apple.randomize_position()

        snake.draw(screen)
        apple.draw(screen)

        # Обновление рекорда
        if snake.score > high_score:
            high_score = snake.score

        # Обновление названия окна
        pygame.display.set_caption(
            f"Змейка - Счёт: {snake.score} Рекорд: {high_score}"
        )

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
