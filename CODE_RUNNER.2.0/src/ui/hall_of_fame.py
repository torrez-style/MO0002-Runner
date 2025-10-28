"""
Salón de la Fama mejorado: muestra nombre del laberinto
"""
import pygame
from src.data.file_manager import load_json, SCORES_FILE

class HallOfFameView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 56)
        self.font_header = pygame.font.SysFont(None, 28)
        self.font_item = pygame.font.SysFont(None, 26)
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
        self.screen.blit(title, ((w - title.get_width())//2, int(h*0.08)))
        
        # Headers
        header = self.font_header.render("POS  JUGADOR           PTS    LABERINTO", True, (180, 180, 180))
        self.screen.blit(header, ((w - header.get_width())//2, int(h*0.18)))
        
        scores = load_json(SCORES_FILE, [])
        if not isinstance(scores, list):
            scores = []
        
        y = int(h*0.25)
        for i, s in enumerate(scores[:10]):
            name = str(s.get("nombre", "-")).upper()[:12]
            pts = int(s.get("puntuacion", 0))
            maze = str(s.get("laberinto", "N/A"))[:10]
            line = f"{i+1:2d}.  {name:<12}  {pts:>6}  {maze}"
            color = (255, 255, 100) if i == 0 else (255, 255, 255)
            surf = self.font_item.render(line, True, color)
            self.screen.blit(surf, ((w - surf.get_width())//2, y))
            y += 30
        
        if not scores:
            empty_msg = self.font_item.render("No hay puntajes registrados", True, (160, 160, 160))
            self.screen.blit(empty_msg, ((w - empty_msg.get_width())//2, int(h*0.45)))
        
        hint = self.font_hint.render("ESC: Volver", True, (200, 200, 200))
        self.screen.blit(hint, ((w - hint.get_width())//2, int(h*0.85)))