"""
Bootstrap: integra efectos de sonido y nombre dinámico del jugador
"""
import random
import os
import pygame
from typing import List, Tuple
from datetime import datetime
from src.ui.maze_renderer import MazeRenderer
from src.data.file_manager import load_json, save_json, SCORES_FILE
from config.settings import settings
from src.audio.sound_manager import sound_manager

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
        self.game_over = False
        # HUD
        self.lives = 3
        self.score = 0
        self.attempts = 1
        self.player_name = "SULA"  # Dinámico
        # Enemigos: velocidad reducida
        self.enemy_tick = 0
        self.enemy_delay = 16
        # VFX
        self.hit_flash_timer = 0
        self.hit_flash_duration = 18

    def set_player_name(self, name: str):
        """Establece el nombre del jugador"""
        self.player_name = name.strip() if name.strip() else "SULA"

    def load_levels(self, path: str = None):
        """
        Carga los niveles desde JSON. Busca en varias rutas si no se provee una.

        Prioridad de rutas:
        1. path (si se pasa)
        2. settings.LEVELS_FILE
        3. assets/config/levels.json
        4. niveles.json (archivo en la raíz del proyecto)
        5. CODE_RUNNER/niveles.json (compatibilidad retro)
        """
        candidates = []
        if path:
            candidates.append(path)
        # preferir la ruta configurada
        try:
            cfg_path = settings.LEVELS_FILE
        except Exception:
            cfg_path = "assets/config/levels.json"
        candidates.append(cfg_path)
        candidates.extend([
            "assets/config/levels.json",
            "niveles.json",
            os.path.join("CODE_RUNNER", "niveles.json")
        ])

        data = {"niveles": []}
        for p in candidates:
            data = load_json(p, {"niveles": []})
            if data and isinstance(data, dict) and data.get("niveles"):
                # mantener la ruta usada (útil para debug)
                # no es estrictamente necesario guardar, sólo devolvemos True/False
                break
        self.levels = data.get("niveles", [])
        if not self.levels:
            return False
        self.level = self.levels[0]
        self.grid = self.level.get("laberinto", [])
        self.entry = tuple(self.level.get("entrada", [1,1]))
        self.exit = tuple(self.level.get("salida", [1,1]))
        self.player = [self.entry[0], self.entry[1]]
        self.colors = self.level.get("colores", self.colors)
        libres = [(x,y) for y,row in enumerate(self.grid) for x,c in enumerate(row) if c==0 and (x,y)!=self.entry]
        random.shuffle(libres)
        count = max(1, int(self.level.get("enemigos", 1)))
        self.enemies = libres[:count]
        est_count = max(1, int(self.level.get("estrellas", 3)))
        libres2 = [p for p in libres if p not in self.enemies]

        self.stars = libres2[:est_count]
        return True

    def _can_move(self, x, y):
        return 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]) and self.grid[y][x] != 1

    def _free_cells(self):
        return [(x,y) for y,row in enumerate(self.grid) for x,c in enumerate(row) if c==0]

    def _enemy_next_step_chase(self, ex, ey):
        px, py = self.player
        dirs = []
        if abs(px-ex) >= abs(py-ey):
            if px > ex:
                dirs.append((1,0))
            if px < ex:
                dirs.append((-1,0))
            if py > ey:
                dirs.append((0,1))
            if py < ey:
                dirs.append((0,-1))
        else:
            if py > ey:
                dirs.append((0,1))
            if py < ey:
                dirs.append((0,-1))
            if px > ex:
                dirs.append((1,0))
            if px < ex:
                dirs.append((-1,0))
        for d in [(1,0),(-1,0),(0,1),(0,-1)]:
            if d not in dirs:
                dirs.append(d)
        for dx, dy in dirs:
            nx, ny = ex+dx, ey+dy
            if self._can_move(nx, ny):
                return nx, ny
        return ex, ey

    def _handle_enemy_collisions(self):
        if self.game_over:
            return
        px, py = self.player
        if (px, py) in self.enemies:
            self.lives -= 1
            self.hit_flash_timer = self.hit_flash_duration
            sound_manager.play_hit()
            libres = [p for p in self._free_cells() if p not in self.enemies]
            if libres:
                self.player[0], self.player[1] = random.choice(libres)
            if self.lives <= 0:
                self._save_score()
                self.game_over = True

    def handle_event(self, event):
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.attempts += 1
                    self.load_levels()
                elif event.key == pygame.K_ESCAPE:
                    return "BACK_TO_MENU"
            return None
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
                    sound_manager.play_move()
                    self.player[0], self.player[1] = nx, ny
                    self.score += 1
                    if (nx, ny) in self.stars:
                        sound_manager.play_star()
                        self.stars.remove((nx, ny))
                        self.score += 10
                    if not self.stars and (nx, ny) == self.exit:
                        sound_manager.play_win()
                        self.score += 50
                        self.win = True
                        self._save_score()
        return None

    def update(self):
        if self.game_over:
            return
        if self.hit_flash_timer > 0:
            self.hit_flash_timer -= 1
        self.enemy_tick += 1
        if self.enemy_tick >= self.enemy_delay:
            self.enemy_tick = 0
            nuevos = []
            ocup = set()
            for ex, ey in self.enemies:
                nx, ny = self._enemy_next_step_chase(ex, ey)
                if (nx, ny) in ocup:
                    nx, ny = ex, ey
                ocup.add((nx, ny))
                nuevos.append((nx, ny))
            self.enemies = nuevos
            self._handle_enemy_collisions()

    def _save_score(self):
        scores = load_json(SCORES_FILE, [])
        if not isinstance(scores, list):
            scores = []
        level_name = self.level.get("nombre", "Nivel 1") if self.level else "Nivel 1"
        entry = {
            "nombre": self.player_name,
            "puntuacion": int(self.score),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "laberinto": level_name
        }
        scores.append(entry)
        scores = sorted(scores, key=lambda s: s.get("puntuacion", 0), reverse=True)[:50]
        save_json(SCORES_FILE, scores)

    def render(self, screen):
        w, h = screen.get_size()
        cols = len(self.grid[0]) if self.grid else 0
        rows = len(self.grid) if self.grid else 0
        cell = self.renderer.cell
        board_w = cols * cell
        board_h = rows * cell
        offset = ((w - board_w)//2, (h - board_h)//2)

        self.renderer.draw_maze(screen, self.grid, self.colors, offset=offset)
        for sx, sy in self.stars:
            rect = pygame.Rect(offset[0] + sx*cell + 10, offset[1] + sy*cell + 10, cell-20, cell-20)
            pygame.draw.rect(screen, (255, 215, 0), rect)
        ex, ey = self.exit
        rect_exit = pygame.Rect(offset[0] + ex*cell + 4, offset[1] + ey*cell + 4, cell-8, cell-8)
        pygame.draw.rect(screen, (0, 180, 120), rect_exit, width=2)
        for e in self.enemies:
            self.renderer.draw_enemy(screen, e, color=tuple(self.colors.get("enemigo", (220,50,50))), offset=offset)
        self.renderer.draw_player(screen, tuple(self.player), offset=offset)

        if self.hit_flash_timer > 0:
            flash = pygame.Surface((w, h), pygame.SRCALPHA)
            alpha = 120 if self.hit_flash_timer > self.hit_flash_duration//2 else 60
            flash.fill((255, 0, 0, alpha))
            screen.blit(flash, (0, 0))

        if self.font_hud is None:
            self.font_hud = pygame.font.SysFont(None, 28)
        hud_text = f"Jugador: {self.player_name}   Vidas: {self.lives}   Puntaje: {self.score}   Estrellas: {len(self.stars)}   Intentos: {self.attempts}"
        hud_surf = self.font_hud.render(hud_text, True, (255,255,255))
        screen.blit(hud_surf, (20, 20))

        if self.win:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 120, 0, 160))
            screen.blit(overlay, (0, 0))
            title_font = pygame.font.SysFont(None, 72)
            info_font = pygame.font.SysFont(None, 36)
            title = title_font.render("GANASTE!", True, (255, 255, 100))
            score_line = info_font.render(f"Puntaje final: {self.score}", True, (230, 230, 230))
            attempts_line = info_font.render(f"Intentos: {self.attempts}", True, (230, 230, 230))
            info1 = info_font.render("ESC: Volver al menu", True, (230, 230, 230))
            screen.blit(title, ((w - title.get_width())//2, int(h*0.32)))
            screen.blit(score_line, ((w - score_line.get_width())//2, int(h*0.42)))
            screen.blit(attempts_line, ((w - attempts_line.get_width())//2, int(h*0.48)))
            screen.blit(info1, ((w - info1.get_width())//2, int(h*0.56)))

        if self.game_over:
            overlay = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            title_font = pygame.font.SysFont(None, 72)
            info_font = pygame.font.SysFont(None, 36)
            title = title_font.render("PERDISTE", True, (255, 100, 100))
            score_line = info_font.render(f"Puntaje final: {self.score}", True, (230, 230, 230))
            attempts_line = info_font.render(f"Intentos: {self.attempts}", True, (230, 230, 230))
            info1 = info_font.render("ENTER: Reiniciar nivel", True, (230, 230, 230))
            info2 = info_font.render("ESC: Volver al menu", True, (230, 230, 230))
            screen.blit(title, ((w - title.get_width())//2, int(h*0.32)))
            screen.blit(score_line, ((w - score_line.get_width())//2, int(h*0.42)))
            screen.blit(attempts_line, ((w - attempts_line.get_width())//2, int(h*0.48)))
            screen.blit(info1, ((w - info1.get_width())//2, int(h*0.56)))
            screen.blit(info2, ((w - info2.get_width())//2, int(h*0.62)))