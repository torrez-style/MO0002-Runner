"""
Vista del juego adaptada a ventana con cálculo de offset centrado
"""
import pygame
from config.settings import settings

class GameView:
    def __init__(self, screen, event_manager):
        self.screen = screen
        self.event_manager = event_manager
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_text = pygame.font.SysFont(None, 28)
        self.bg_color = (30, 30, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pass

    def update(self, delta_time: float):
        pass

    def render(self):
        w, h = self.screen.get_size()
        self.screen.fill(self.bg_color)
        title = self.font_title.render("Vista del juego", True, (240, 240, 240))
        self.screen.blit(title, ((w - title.get_width()) // 2, int(h*0.07)))
        info = [
            "Laberinto y elementos se adaptan al tamaño de ventana.",
            "El render del nivel se centra usando offsets calculados.",
        ]
        y = int(h*0.15)
        for line in info:
            surf = self.font_text.render(line, True, (210, 210, 210))
            self.screen.blit(surf, ((w - surf.get_width()) // 2, y))
            y += 34
