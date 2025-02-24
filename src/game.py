# Game class encapsulating the main game loop and state
import sys
import pygame
from settings import WIDTH, HEIGHT, BLACK, WHITE, POWER_PELLET_DURATION, LABYRINTH_GRID, CELL_SIZE, VELOCITY, YELLOW, RED, PINK, CYAN, ORANGE
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
        self.ghosts = [
            Ghost((6, 6), RED, "Blinky"),
            Ghost((7, 6), PINK, "Pinky"),
            Ghost((6, 7), CYAN, "Inky"),
            Ghost((7, 7), ORANGE, "Clyde")
        ]
        self.score = 0
        self.lives = 3
        self.power_pellet_active = False
        self.power_pellet_timer = 0
        self.game_over = False
        self.won = False

    def collision(self, x, y):
        col = int(x // CELL_SIZE)
        row = int(y // CELL_SIZE)
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
                if abs(self.pacman.x - point[0]) < 20 and abs(self.pacman.y - point[1]) < 20:
                    self.points.remove(point)
                    self.score += 10

            # Check collision with power pellets
            for pellet in self.power_pellets[:]:
                if abs(self.pacman.x - pellet[0]) < 20 and abs(self.pacman.y - pellet[1]) < 20:
                    self.power_pellets.remove(pellet)
                    self.score += 50
                    self.power_pellet_active = True
                    self.power_pellet_timer = pygame.time.get_ticks()
                    for ghost in self.ghosts:
                        ghost.frightened = True

            # Check collision with ghosts
            for ghost in self.ghosts:
                if abs(self.pacman.x - ghost.x) < 40 and abs(self.pacman.y - ghost.y) < 40:
                    if ghost.frightened:
                        new_pos = (6, 6) if ghost.name in ["Blinky", "Pinky"] else (6, 7) if ghost.name == "Inky" else (7, 7)
                        ghost.reset(new_pos)
                        self.score += 200
                    else:
                        self.lives -= 1
                        self.pacman.__init__()
                        if self.lives <= 0:
                            self.game_over = True

            # Check win condition
            if not self.points and not self.power_pellets:
                self.won = True

            # Manage power pellet duration
            if self.power_pellet_active and pygame.time.get_ticks() - self.power_pellet_timer > POWER_PELLET_DURATION:
                self.power_pellet_active = False
                for ghost in self.ghosts:
                    ghost.frightened = False

    def draw(self):
        self.screen.fill(BLACK)
        draw_labyrinth(self.screen)
        draw_points(self.screen, self.points)
        draw_power_pellets(self.screen, self.power_pellets)
        self.pacman.draw(self.screen, pygame.time.get_ticks())
        for ghost in self.ghosts:
            ghost.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        
        if self.game_over:
            over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
            self.screen.blit(over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        elif self.won:
            win_text = self.font.render("You Won! Press R to restart", True, WHITE)
            self.screen.blit(win_text, (WIDTH // 2 - 200, HEIGHT // 2))

        pygame.display.flip()

    def run(self):
        while True:
            self.process_events()
            self.update()
            self.draw()
            self.clock.tick(60)
