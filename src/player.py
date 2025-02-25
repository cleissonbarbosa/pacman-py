import pygame
import math
from settings import CELL_SIZE, VELOCITY, YELLOW, UI_BAR_HEIGHT


class Pacman:
    def __init__(self, init_cell=(1, 1)):
        self.x = init_cell[0] * CELL_SIZE + CELL_SIZE // 2
        # Adjust y by adding UI_BAR_HEIGHT
        self.y = init_cell[1] * CELL_SIZE + CELL_SIZE // 2 + UI_BAR_HEIGHT
        self.speed = VELOCITY
        self.direction = "right"
        self.radius = 20

    def move(self, keys, collision_func):
        new_x, new_y = self.x, self.y
        if keys[pygame.K_LEFT]:
            new_x -= self.speed
            self.direction = "left"
        elif keys[pygame.K_RIGHT]:
            new_x += self.speed
            self.direction = "right"
        elif keys[pygame.K_UP]:
            new_y -= self.speed
            self.direction = "up"
        elif keys[pygame.K_DOWN]:
            new_y += self.speed
            self.direction = "down"

        if not collision_func(new_x, new_y):
            self.x, self.y = new_x, new_y

    def draw(self, surface, current_time):
        # Animate mouth opening/closing
        mouth_open = math.sin(current_time / 200) > 0
        if mouth_open:
            angles = {
                "right": (0.2 * math.pi, 1.8 * math.pi),
                "left": (1.2 * math.pi, 0.8 * math.pi),
                "up": (0.7 * math.pi, 0.3 * math.pi),
                "down": (1.7 * math.pi, 1.3 * math.pi),
            }
            start_angle, end_angle = angles.get(
                self.direction, (0.2 * math.pi, 1.8 * math.pi)
            )
            pygame.draw.arc(
                surface,
                YELLOW,
                (
                    self.x - self.radius,
                    self.y - self.radius,
                    self.radius * 2,
                    self.radius * 2,
                ),
                start_angle,
                end_angle,
                20,
            )
        else:
            pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.radius)
