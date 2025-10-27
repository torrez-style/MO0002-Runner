"""
Vista principal de juego (placeholder mínimo)
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
            # Dejar al GameEngine cambiar estado; placeholder sin transición directa
            pass

    def update(self, delta_time: float):
        pass

    def render(self):
        self.screen.fill(self.bg_color)
        title = self.font_title.render("Maze Runner - Vista", True, (240, 240, 240))
        self.screen.blit(title, (40, 40))
        info = [
            "Este es un placeholder de la vista del juego.",
            "Integraremos laberinto, jugador, enemigos y HUD en las siguientes fases.",
            "Presione ESC para volver al menú (próxima iteración)."
        ]
        y = 120
        for line in info:
            surf = self.font_text.render(line, True, (210, 210, 210))
            self.screen.blit(surf, (40, y))
            y += 36
