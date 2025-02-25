import pygame
from settings import CELL_SIZE, LABYRINTH_GRID, BLUE, WHITE, UI_BAR_HEIGHT


def draw_labyrinth(surface):
    for y, row in enumerate(LABYRINTH_GRID):
        for x, cell in enumerate(row):
            if cell == 1:
                # Offset y coordinate by UI_BAR_HEIGHT
                pygame.draw.rect(
                    surface,
                    BLUE,
                    (
                        x * CELL_SIZE,
                        y * CELL_SIZE + UI_BAR_HEIGHT,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )


def create_points():
    points = []
    power_pellets = []
    for y, row in enumerate(LABYRINTH_GRID):
        for x, cell in enumerate(row):
            if cell == 0:
                point = (
                    x * CELL_SIZE + CELL_SIZE // 2,
                    y * CELL_SIZE + CELL_SIZE // 2 + UI_BAR_HEIGHT,
                )
                points.append(point)
                if (x, y) in [(1, 1), (12, 1), (1, 12), (12, 12)]:
                    power_pellets.append(point)
    return points, power_pellets


def draw_points(surface, points):
    for point in points:
        pygame.draw.circle(surface, WHITE, point, 5)


def draw_power_pellets(surface, pellets):
    for pellet in pellets:
        pygame.draw.circle(surface, WHITE, pellet, 10)
