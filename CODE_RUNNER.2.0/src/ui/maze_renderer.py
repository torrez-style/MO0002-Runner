"""
Dibujo básico de laberinto, jugador y enemigos
"""
import pygame

class MazeRenderer:
    def __init__(self, cell_size=32):
        self.cell = cell_size

    def draw_maze(self, screen, grid, colors, offset=(40, 40)):
        ox, oy = offset
        wall = tuple(colors.get("pared", (80, 80, 80)))
        floor = tuple(colors.get("suelo", (220, 230, 245)))
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                rect = pygame.Rect(ox + x*self.cell, oy + y*self.cell, self.cell, self.cell)
                pygame.draw.rect(screen, floor if c != 1 else wall, rect)

    def draw_player(self, screen, pos, color=(50, 150, 255), offset=(40, 40)):
        ox, oy = offset
        x, y = pos
        rect = pygame.Rect(ox + x*self.cell+4, oy + y*self.cell+4, self.cell-8, self.cell-8)
        pygame.draw.rect(screen, color, rect)

    def draw_enemy(self, screen, pos, color=(220, 50, 50), offset=(40, 40)):
        ox, oy = offset
        x, y = pos
        rect = pygame.Rect(ox + x*self.cell+6, oy + y*self.cell+6, self.cell-12, self.cell-12)
        pygame.draw.rect(screen, color, rect)
