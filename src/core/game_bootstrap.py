"""
Bootstrap ampliado: movimiento con flechas, estrellas, HUD y victoria por salida
"""
import random
import pygame
from typing import List, Tuple
from src.ui.maze_renderer import MazeRenderer
from src.data.file_manager import load_json

class GameBootstrap:
    def __init__(self):
        self.levels = []
        self.level = None
        self.grid: List[List[int]] = []
        self.entry = (1, 1)
        self.exit = (1, 1)
        self.player = [1, 1]
        self.enemies: List[Tuple[int,int]] = []
        self.colors = {"pared": (80,80,80), "suelo": (220,230,245), "enemigo": (220,50,50)}
        self.renderer = MazeRenderer(cell_size=32)
        self.font_hud = None
        self.stars: List[Tuple[int,int]] = []
        self.win = False

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
        # Colocar estrellas en celdas libres (por defecto 3)
        est_count = max(1, int(self.level.get("estrellas", 3)))
        libres2 = [p for p in libres if p not in self.enemies]
        random.shuffle(libres2)
        self.stars = libres2[:est_count]
        self.win = False
        return True

    def _can_move(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]) and self.grid[y][x] != 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            dx = dy = 0
            if event.key == pygame.K_UP:
                dy = -1
            elif event.key == pygame.K_DOWN:
                dy = 1
            elif event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            if dx or dy:
                nx, ny = self.player[0] + dx, self.player[1] + dy
                if self._can_move(nx, ny):
                    self.player[0], self.player[1] = nx, ny
                    # Recolectar estrella
                    if (nx, ny) in self.stars:
                        self.stars.remove((nx, ny))
                    # Victoria: sin estrellas y en salida
                    if not self.stars and (nx, ny) == self.exit:
                        self.win = True

    def update(self):
        pass

    def render(self, screen):
        # Calcular offset para centrar el laberinto en la ventana
        w, h = screen.get_size()
        cols = len(self.grid[0]) if self.grid else 0
        rows = len(self.grid) if self.grid else 0
        cell = self.renderer.cell
        board_w = cols * cell
        board_h = rows * cell
        offset = ((w - board_w)//2, (h - board_h)//2)

        # Dibujo del laberinto y entidades
        self.renderer.draw_maze(screen, self.grid, self.colors, offset=offset)
        # Estrellas
        for sx, sy in self.stars:
            rect = pygame.Rect(offset[0] + sx*cell + 10, offset[1] + sy*cell + 10, cell-20, cell-20)
            pygame.draw.rect(screen, (255, 215, 0), rect)
        # Salida
        ex, ey = self.exit
        rect_exit = pygame.Rect(offset[0] + ex*cell + 4, offset[1] + ey*cell + 4, cell-8, cell-8)
        pygame.draw.rect(screen, (0, 180, 120), rect_exit, width=2)
        # Enemigos
        for e in self.enemies:
            self.renderer.draw_enemy(screen, e, color=tuple(self.colors.get("enemigo", (220,50,50))), offset=offset)
        # Jugador
        self.renderer.draw_player(screen, tuple(self.player), offset=offset)

        # HUD
        if self.font_hud is None:
            self.font_hud = pygame.font.SysFont(None, 28)
        hud_text = f"Estrellas restantes: {len(self.stars)}"
        hud_surf = self.font_hud.render(hud_text, True, (255,255,255))
        screen.blit(hud_surf, (20, 20))

        if self.win:
            win_font = pygame.font.SysFont(None, 56)
            msg = "Nivel completado. Presione ESC para volver al menú."
            win_surf = win_font.render(msg, True, (255,255,255))
            screen.blit(win_surf, ((w - win_surf.get_width())//2, int(h*0.85)))
