"""
Menú principal (placeholder mínimo)
"""
import pygame
from config.settings import settings

class MenuPrincipal:
    def __init__(self, screen, event_manager):
        self.screen = screen
        self.event_manager = event_manager
        self.options = ["JUGAR", "SALON DE LA FAMA", "ADMINISTRACION", "SALIR"]
        self.index = 0
        self.font_title = pygame.font.SysFont(None, 56)
        self.font_opt = pygame.font.SysFont(None, 36)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.index = (self.index - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.index = (self.index + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                # Publicar eventos en siguientes iteraciones
                pass

    def update(self, delta_time: float):
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        title = self.font_title.render("Maze Runner", True, (255, 255, 255))
        self.screen.blit(title, (60, 60))
        y = 160
        for i, opt in enumerate(self.options):
            color = (255, 255, 0) if i == self.index else (200, 200, 200)
            surf = self.font_opt.render(opt, True, color)
            self.screen.blit(surf, (60, y))
            y += 48
