import sys
import pygame
import math
from settings import (
    WIDTH,
    HEIGHT,
    BLACK,
    WHITE,
    POWER_PELLET_DURATION,
    LABYRINTH_GRID,
    CELL_SIZE,
    VELOCITY,
    YELLOW,
    RED,
    PINK,
    CYAN,
    ORANGE,
    GRAY,
    UI_BAR_HEIGHT,
)
from maze import draw_labyrinth, create_points, draw_points, draw_power_pellets
from player import Pacman
from ghost import Ghost


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.font = pygame.font.SysFont(None, 36)
        self.clock = pygame.time.Clock()
        self.init_game()

    def init_game(self):
        self.points, self.power_pellets = create_points()
        self.pacman = Pacman()
        # Update ghost spawn positions to safe cells in the maze
        self.ghosts = [
            Ghost((6, 5), RED, "Blinky"),
            Ghost((7, 5), PINK, "Pinky"),
            Ghost((6, 6), CYAN, "Inky"),
            Ghost((12, 6), ORANGE, "Clyde"),
        ]
        self.score = 0
        self.lives = 3
        self.power_pellet_active = False
        self.power_pellet_timer = 0
        self.game_over = False
        self.won = False

    def collision(self, x, y):
        # Adjust y by subtracting UI_BAR_HEIGHT since maze is drawn offset
        y_adjusted = y - UI_BAR_HEIGHT
        col = int(x // CELL_SIZE)
        row = int(y_adjusted // CELL_SIZE)
        if 0 <= row < len(LABYRINTH_GRID) and 0 <= col < len(LABYRINTH_GRID[0]):
            return LABYRINTH_GRID[row][col] == 1
        return True

    def reset_game(self):
        self.init_game()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and (self.game_over or self.won):
                if event.key == pygame.K_r:
                    self.reset_game()

    def update(self):
        if not (self.game_over or self.won):
            keys = pygame.key.get_pressed()
            self.pacman.move(keys, self.collision)

            # Update ghosts
            for ghost in self.ghosts:
                ghost.update(self.collision)

            # Check collision with points
            for point in self.points[:]:
                if math.hypot(self.pacman.x - point[0], self.pacman.y - point[1]) < self.pacman.radius:
                    self.points.remove(point)
                    self.score += 10

            # Check collision with power pellets
            for pellet in self.power_pellets[:]:
                if math.hypot(self.pacman.x - pellet[0], self.pacman.y - pellet[1]) < self.pacman.radius:
                    self.power_pellets.remove(pellet)
                    self.score += 50
                    self.power_pellet_active = True
                    self.power_pellet_timer = pygame.time.get_ticks()
                    for ghost in self.ghosts:
                        ghost.frightened = True

            # Check collision with ghosts
            for ghost in self.ghosts:
                if (
                    abs(self.pacman.x - ghost.x) < 40
                    and abs(self.pacman.y - ghost.y) < 40
                ):
                    if ghost.frightened and not ghost.is_dying and not ghost.respawning:
                        ghost.start_death_animation()
                        self.score += 200
                    elif not ghost.frightened and not ghost.is_dying and not ghost.respawning:
                        self.lives -= 1
                        self.pacman.__init__()
                        if self.lives <= 0:
                            self.game_over = True

            # Check win condition
            if not self.points and not self.power_pellets:
                self.won = True

            # Manage power pellet duration
            if (
                self.power_pellet_active
                and pygame.time.get_ticks() - self.power_pellet_timer
                > POWER_PELLET_DURATION
            ):
                self.power_pellet_active = False
                for ghost in self.ghosts:
                    ghost.frightened = False

    def draw_heart(self, surface, x, y, size, color):
        # Draw two circles for the upper lobes of the heart
        circle_radius = size // 4
        left_circle_center = (x - size // 4, y - size // 4)
        right_circle_center = (x + size // 4, y - size // 4)
        pygame.draw.circle(surface, color, left_circle_center, circle_radius)
        pygame.draw.circle(surface, color, right_circle_center, circle_radius)
        # Draw the bottom triangle of the heart
        triangle_points = [
            (x - size // 2, y - size // 4),
            (x + size // 2, y - size // 4),
            (x, y + size // 2)
        ]
        pygame.draw.polygon(surface, color, triangle_points)

    def draw(self):
        # Fill background
        self.screen.fill(BLACK)

        # Draw top UI bar for score and lives
        ui_rect = pygame.Rect(0, 0, WIDTH, UI_BAR_HEIGHT)
        pygame.draw.rect(self.screen, BLACK, ui_rect)  # Draw UI background
        pygame.draw.line(self.screen, WHITE, (0, UI_BAR_HEIGHT), (WIDTH, UI_BAR_HEIGHT), 2)  # Divider

        # Draw score on the UI bar
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, (UI_BAR_HEIGHT - score_text.get_height()) // 2))

        # Draw hearts for lives using pygame.draw
        heart_size = 20
        spacing = 5
        total_width = self.lives * heart_size + (self.lives - 1) * spacing
        start_x = WIDTH - 10 - total_width + heart_size // 2
        center_y = UI_BAR_HEIGHT // 2
        for i in range(self.lives):
            heart_x = start_x + i * (heart_size + spacing)
            self.draw_heart(self.screen, heart_x, center_y, heart_size, RED)

        # Draw maze and game elements (maze and items offsets are already adjusted using UI_BAR_HEIGHT in maze.py)
        draw_labyrinth(self.screen)
        draw_points(self.screen, self.points)
        draw_power_pellets(self.screen, self.power_pellets)
        self.pacman.draw(self.screen, pygame.time.get_ticks())
        for ghost in self.ghosts:
            ghost.draw(self.screen)

        # Draw end game messages
        if self.game_over:
            over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
            self.screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2))
        elif self.won:
            win_text = self.font.render("You Won! Press R to restart", True, WHITE)
            self.screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while True:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(60)
