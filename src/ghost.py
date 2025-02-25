import pygame
import math
from settings import CELL_SIZE, VELOCITY, UI_BAR_HEIGHT
import random


class Ghost:
    def __init__(self, init_cell, color, name):
        self.init_cell = init_cell
        self.x = init_cell[0] * CELL_SIZE + CELL_SIZE // 2
        # Add UI_BAR_HEIGHT offset to y coordinate
        self.y = init_cell[1] * CELL_SIZE + CELL_SIZE // 2 + UI_BAR_HEIGHT
        self.color = color
        self.name = name
        self.speed = VELOCITY - 1
        self.frightened = False
        # Random initial direction
        self.direction = random.choice(["left", "right", "up", "down"])
        self.animation_offset = 0
        self.animation_speed = 0.008

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

        # Atualiza a animação de flutuação
        self.animation_offset = math.sin(pygame.time.get_ticks() * self.animation_speed) * 3

    def draw(self, surface):
        # Draw ghost with a ghost-like shape
        ghost_color = (0, 0, 255) if self.frightened else self.color
        x = int(self.x)
        # Aplica o offset de animação no y
        y = int(self.y + self.animation_offset)
        r = CELL_SIZE // 2
        
        # Draw head as a circle shifted upward
        head_center = (x, y - r // 2)
        pygame.draw.circle(surface, ghost_color, head_center, r)
        
        # Draw body rectangle below the head
        body_rect = pygame.Rect(x - r, y - r // 2, 2 * r, r)
        pygame.draw.rect(surface, ghost_color, body_rect)
        
        # Draw scalloped bottom with wave animation
        num_teeth = 5
        step = (2 * r) / (num_teeth - 1)
        wave_offset = math.sin(pygame.time.get_ticks() * 0.01) * 2
        for i in range(num_teeth):
            tooth_offset = math.sin(pygame.time.get_ticks() * 0.01 + i) * 2
            tooth_center = (int(x - r + i * step), y + r // 2 + tooth_offset)
            pygame.draw.circle(surface, ghost_color, tooth_center, r // 4)
        
        # Draw eyes with blinking animation
        eye_radius = r // 4
        left_eye_center = (x - r // 2, y - r // 2)
        right_eye_center = (x + r // 2, y - r // 2)
        
        # Blinking animation a cada 3 segundos
        blink = (pygame.time.get_ticks() % 3000) < 100
        if not blink:
            pygame.draw.circle(surface, (255, 255, 255), left_eye_center, eye_radius)
            pygame.draw.circle(surface, (255, 255, 255), right_eye_center, eye_radius)
            
            # Draw pupils with direction
            pupil_radius = r // 8
            pupil_offset = eye_radius // 2
            
            # Calculate pupil positions based on direction
            if self.direction == "right":
                left_pupil = (left_eye_center[0] + pupil_offset, left_eye_center[1])
                right_pupil = (right_eye_center[0] + pupil_offset, right_eye_center[1])
            elif self.direction == "left":
                left_pupil = (left_eye_center[0] - pupil_offset, left_eye_center[1])
                right_pupil = (right_eye_center[0] - pupil_offset, right_eye_center[1])
            elif self.direction == "up":
                left_pupil = (left_eye_center[0], left_eye_center[1] - pupil_offset)
                right_pupil = (right_eye_center[0], right_eye_center[1] - pupil_offset)
            else:  # down
                left_pupil = (left_eye_center[0], left_eye_center[1] + pupil_offset)
                right_pupil = (right_eye_center[0], right_eye_center[1] + pupil_offset)
            
            pygame.draw.circle(surface, (0, 0, 0), left_pupil, pupil_radius)
            pygame.draw.circle(surface, (0, 0, 0), right_pupil, pupil_radius)
        else:
            # Desenha olhos fechados (linha horizontal)
            pygame.draw.line(surface, (0, 0, 0), 
                           (left_eye_center[0] - eye_radius//2, left_eye_center[1]),
                           (left_eye_center[0] + eye_radius//2, left_eye_center[1]), 2)
            pygame.draw.line(surface, (0, 0, 0),
                           (right_eye_center[0] - eye_radius//2, right_eye_center[1]),
                           (right_eye_center[0] + eye_radius//2, right_eye_center[1]), 2)
    
    def reset(self, init_cell):
        self.init_cell = init_cell
        self.x = init_cell[0] * CELL_SIZE + CELL_SIZE // 2
        self.y = init_cell[1] * CELL_SIZE + CELL_SIZE // 2 + UI_BAR_HEIGHT
        self.frightened = False
        self.direction = random.choice(["left", "right", "up", "down"])
