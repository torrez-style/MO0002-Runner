"""
Pantalla del Salón de la Fama (Top 10) con opción de volver con ESC
"""
import pygame
from src.data.file_manager import load_json, SCORES_FILE

class HallOfFameView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 56)
        self.font_item = pygame.font.SysFont(None, 32)
        self.font_hint = pygame.font.SysFont(None, 26)
        self.bg_color = (0, 0, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "BACK"
        return None

    def render(self):
        w, h = self.screen.get_size()
        self.screen.fill(self.bg_color)
        title = self.font_title.render("SALON DE LA FAMA", True, (255, 255, 0))
        self.screen.blit(title, ((w - title.get_width())//2, int(h*0.12)))
        scores = load_json(SCORES_FILE, [])
        if not isinstance(scores, list):
            scores = []
        y = int(h*0.25)
        for i, s in enumerate(scores[:10]):
            name = str(s.get("nombre", "-")).upper()[:18]
            pts = int(s.get("puntuacion", 0))
            line = f"{i+1:2d}. {name:<18}  {pts:>6}"
            surf = self.font_item.render(line, True, (255, 255, 255))
            self.screen.blit(surf, ((w - surf.get_width())//2, y))
            y += 36
        hint = self.font_hint.render("ESC: Volver", True, (200, 200, 200))
        self.screen.blit(hint, ((w - hint.get_width())//2, int(h*0.85)))
