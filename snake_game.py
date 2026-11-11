import pygame
import random
import sys

# Game constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (76, 175, 80)
DARK_GREEN = (46, 125, 50)
RED = (244, 67, 54)
BLUE = (33, 150, 243)
YELLOW = (255, 193, 7)


class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.snake = [
            (GRID_WIDTH // 2 * CELL_SIZE, GRID_HEIGHT // 2 * CELL_SIZE),
            ((GRID_WIDTH // 2 - 1) * CELL_SIZE, GRID_HEIGHT // 2 * CELL_SIZE),
            ((GRID_WIDTH // 2 - 2) * CELL_SIZE, GRID_HEIGHT // 2 * CELL_SIZE),
        ]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = (CELL_SIZE, 0)
        self.food = self.spawn_food()
        self.score = 0
        self.game_over = False
        self.message = "Use arrow keys to move"

    def spawn_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_over and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset()
                    continue

                if event.key == pygame.K_UP:
                    self.next_direction = (0, -CELL_SIZE)
                elif event.key == pygame.K_DOWN:
                    self.next_direction = (0, CELL_SIZE)
                elif event.key == pygame.K_LEFT:
                    self.next_direction = (-CELL_SIZE, 0)
                elif event.key == pygame.K_RIGHT:
                    self.next_direction = (CELL_SIZE, 0)

        return True

    def update(self):
        if self.game_over:
            return

        # prevent reversing direction instantly
        if (
            self.next_direction[0] != -self.direction[0]
            or self.next_direction[1] != -self.direction[1]
        ):
            self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        move_x, move_y = self.direction
        new_head = (head_x + move_x, head_y + move_y)

        # wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WINDOW_WIDTH
            or new_head[1] < 0
            or new_head[1] >= WINDOW_HEIGHT
        ):
            self.game_over = True
            self.message = "Game Over! Press Enter to restart"
            return

        # self collision
        if new_head in self.snake:
            self.game_over = True
            self.message = "Game Over! Press Enter to restart"
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
        else:
            self.snake.pop()

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

    def draw_snake(self):
        for index, segment in enumerate(self.snake):
            color = GREEN if index == 0 else DARK_GREEN
            rect = pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.screen, color, rect, border_radius=4)
            if index == 0:
                pygame.draw.rect(self.screen, BLUE, rect.inflate(-8, -8), border_radius=4)

    def draw_food(self):
        rect = pygame.Rect(self.food[0], self.food[1], CELL_SIZE, CELL_SIZE)
        pygame.draw.ellipse(self.screen, RED, rect)

    def draw_score(self):
        font = pygame.font.SysFont("arial", 24, bold=True)
        text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))

    def draw_message(self):
        if not self.game_over:
            return
        font = pygame.font.SysFont("arial", 36, bold=True)
        text = font.render(self.message, True, YELLOW)
        rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, rect)

    def render(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_food()
        self.draw_snake()
        self.draw_score()
        self.draw_message()
        pygame.display.flip()

    def run(self):
        while True:
            running = self.handle_events()
            if not running:
                pygame.quit()
                sys.exit()

            self.update()
            self.render()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
