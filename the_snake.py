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
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки
SPEED = 10

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class Apple:
    """Класс для яблока."""

    def __init__(self, snake_positions):
        self.position = self.randomize_position(snake_positions)
        self.color = APPLE_COLOR

    def randomize_position(self, snake_positions):
        while True:
            x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            if (x, y) not in snake_positions:
                return (x, y)

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake:
    """Класс для змейки."""

    def __init__(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        return self.positions[0]

    def move(self):
        cur = self.get_head_position()
        x, y = self.direction
        new_head = (
            ((cur[0] + (x * GRID_SIZE)) % SCREEN_WIDTH),
            ((cur[1] + (y * GRID_SIZE)) % SCREEN_HEIGHT),
        )
        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self):
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, SNAKE_COLOR, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.next_direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.next_direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.next_direction = RIGHT

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None


def load_highscore():
    try:
        with open("highscore.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0


def save_highscore(score):
    with open("highscore.txt", "w") as file:
        file.write(str(score))


def main():
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    score = 0
    high_score = load_highscore()

    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)

        snake.handle_keys()
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple = Apple(snake.positions)
            score += 1
            if score > high_score:
                high_score = score
                save_highscore(high_score)

        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()
            score = 0

        snake.draw()
        apple.draw()

        pygame.display.set_caption(
            f'Змейка - Счёт: {score} Рекорд: {high_score}'
        )
        pygame.display.update()


if __name__ == '__main__':
    main()
