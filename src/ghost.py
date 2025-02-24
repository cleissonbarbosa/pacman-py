import pygame
from settings import CELL_SIZE, VELOCITY
import random


class Ghost:
    def __init__(self, init_cell, color, name):
        self.init_cell = init_cell
        self.x = init_cell[0] * CELL_SIZE + CELL_SIZE // 2
        self.y = init_cell[1] * CELL_SIZE + CELL_SIZE // 2
        self.color = color
        self.name = name
        self.speed = VELOCITY - 1
        self.frightened = False
        # Random initial direction
        self.direction = random.choice(["left", "right", "up", "down"])

    def update(self, collision_func):
        # Simple movement: move in current direction, if collide, change direction randomly
        new_x, new_y = self.x, self.y
        if self.direction == "left":
            new_x -= self.speed
        elif self.direction == "right":
            new_x += self.speed
        elif self.direction == "up":
            new_y -= self.speed
        elif self.direction == "down":
            new_y += self.speed

        if not collision_func(new_x, new_y):
            self.x, self.y = new_x, new_y
        else:
            self.direction = random.choice(["left", "right", "up", "down"])

    def draw(self, surface):
        # Draw ghost as a circle; if frightened, show blue color
        color = (0, 0, 255) if self.frightened else self.color
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), CELL_SIZE // 2)

    def reset(self, init_cell):
        self.init_cell = init_cell
        self.x = init_cell[0] * CELL_SIZE + CELL_SIZE // 2
        self.y = init_cell[1] * CELL_SIZE + CELL_SIZE // 2
        self.frightened = False
        self.direction = random.choice(["left", "right", "up", "down"])
