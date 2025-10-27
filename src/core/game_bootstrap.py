"""
Bootstrap ampliado con IA enemiga simple, HUD de vidas/puntaje y guardado de salón de la fama
"""
import random
import pygame
from typing import List, Tuple
from datetime import datetime
from src.ui.maze_renderer import MazeRenderer
from src.data.file_manager import load_json, save_json, SCORES_FILE

PLAYER_NAME = "SULA"

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
        # HUD y lógica
        self.lives = 3
        self.score = 0
        # Enemigos
        self.enemy_tick = 0
        self.enemy_delay = 12

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
        # Reset lógica
        self.lives = 3
        self.score = 0
        self.win = False
        return True

    def _can_move(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]) and self.grid[y][x] != 1

    def _free_cells(self):
        return [(x,y) for y,row in enumerate(self.grid) for x,c in enumerate(row) if c==0]

    def _enemy_next_step(self, ex, ey):
        # Heurística simple hacia el jugador con fallback a pasos alternos
        px, py = self.player
        dirs = []
        if px > ex: dirs.append((1,0))
        if px < ex: dirs.append((-1,0))
        if py > ey: dirs.append((0,1))
        if py < ey: dirs.append((0,-1))
        # Completar con alternativas ortogonales para probar huecos
        for d in [(1,0),(-1,0),(0,1),(0,-1)]:
            if d not in dirs: dirs.append(d)
        # Intentar en orden
        for dx, dy in dirs:
            nx, ny = ex+dx, ey+dy
            if self._can_move(nx, ny) and (nx,ny) != tuple(self.player):
                # evitar chocar con otro enemigo si es posible
                if (nx,ny) not in self.enemies:
                    return nx, ny
        return ex, ey

    def _handle_enemy_collisions(self):
        # Si algún enemigo alcanza al jugador
        if tuple(self.player) in self.enemies:
            self.lives -= 1
            # Reposicionar jugador a celda libre aleatoria
            libres = [p for p in self._free_cells() if p not in self.enemies]
            if libres:
                self.player[0], self.player[1] = random.choice(libres)
            if self.lives <= 0:
                # Fin de juego: guardar score y marcar win como False
                self._save_score()
                self.win = False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            dx = dy = 0
            if event.key == pygame.K_UP: dy = -1
            elif event.key == pygame.K_DOWN: dy = 1
            elif event.key == pygame.K_LEFT: dx = -1
            elif event.key == pygame.K_RIGHT: dx = 1
            if dx or dy:
                nx, ny = self.player[0] + dx, self.player[1] + dy
                if self._can_move(nx, ny):
                    self.player[0], self.player[1] = nx, ny
                    self.score += 1  # puntos por movimiento
                    # Recolectar estrella
                    if (nx, ny) in self.stars:
                        self.stars.remove((nx, ny))
                        self.score += 10
                    # Victoria: sin estrellas y en salida
                    if not self.stars and (nx, ny) == self.exit:
                        self.score += 50
                        self.win = True
                        self._save_score()

    def update(self):
        # Movimiento de enemigos por tick
        self.enemy_tick += 1
        if self.enemy_tick >= self.enemy_delay:
            self.enemy_tick = 0
            nuevos = []
            ocup = set()
            for ex, ey in self.enemies:
                nx, ny = self._enemy_next_step(ex, ey)
                if (nx, ny) in ocup:
                    nx, ny = ex, ey
                ocup.add((nx, ny))
                nuevos.append((nx, ny))
            self.enemies = nuevos
            # Colisiones
            self._handle_enemy_collisions()

    def _save_score(self):
        scores = load_json(SCORES_FILE, [])
        if not isinstance(scores, list):
            scores = []
        entry = {
            "nombre": PLAYER_NAME,
            "puntuacion": int(self.score),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        scores.append(entry)
        # Ordenar y guardar top 50 para no crecer indefinidamente
        scores = sorted(scores, key=lambda s: s.get("puntuacion", 0), reverse=True)[:50]
        save_json(SCORES_FILE, scores)

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
        hud_text = f"Vidas: {self.lives}   Puntaje: {self.score}   Estrellas: {len(self.stars)}"
        hud_surf = self.font_hud.render(hud_text, True, (255,255,255))
        screen.blit(hud_surf, (20, 20))

        if self.win:
            win_font = pygame.font.SysFont(None, 52)
            msg = "Nivel completado. Presione ESC para volver al menú."
            win_surf = win_font.render(msg, True, (255,255,255))
            screen.blit(win_surf, ((w - win_surf.get_width())//2, int(h*0.85)))
