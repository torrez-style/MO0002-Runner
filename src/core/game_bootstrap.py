"""
Conector rápido: carga niveles, cambia de menú a juego y dibuja nivel 1
"""
import json
import os
import random
import pygame
from config.settings import settings
from src.ui.maze_renderer import MazeRenderer
from src.data.file_manager import load_json

class GameBootstrap:
    def __init__(self):
        self.levels = []
        self.level = None
        self.grid = []
        self.entry = (1, 1)
        self.exit = (1, 1)
        self.player = [1, 1]
        self.enemies = []
        self.colors = {"pared": (80,80,80), "suelo": (220,230,245), "enemigo": (220,50,50)}
        self.renderer = MazeRenderer(cell_size=32)

    def load_levels(self, path="assets/config/levels.json"):
        data = load_json(path, {"niveles": []})
        self.levels = data.get("niveles", [])
        if not self.levels:
            return False
        self.level = self.levels[0]
        self.grid = self.level.get("laberinto", [])
        self.entry = tuple(self.level.get("entrada", [1,1]))
        self.exit = tuple(self.level.get("salida", [1,1]))
        self.player = [self.entry[0], self.entry[1]]
        self.colors = self.level.get("colores", self.colors)
        # Enemigos básicos en celdas libres lejos de la entrada
        count = max(1, int(self.level.get("enemigos", 1)))
        libres = [(x,y) for y,row in enumerate(self.grid) for x,c in enumerate(row) if c==0 and (x,y)!=self.entry]
        random.shuffle(libres)
        self.enemies = libres[:count]
        return True

    def update(self):
        pass

    def render(self, screen):
        self.renderer.draw_maze(screen, self.grid, self.colors)
        self.renderer.draw_player(screen, tuple(self.player))
        for e in self.enemies:
            self.renderer.draw_enemy(screen, e, color=tuple(self.colors.get("enemigo", (220,50,50))))
