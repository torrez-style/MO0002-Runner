"""
Menú principal centrado horizontalmente
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
                pass

    def update(self, delta_time: float):
        pass

    def render(self):
        w, h = self.screen.get_size()
        self.screen.fill((0, 0, 0))
        title_surf = self.font_title.render("Maze Runner", True, (255, 255, 255))
        title_x = (w - title_surf.get_width()) // 2
        self.screen.blit(title_surf, (title_x, int(h*0.15)))
        start_y = int(h*0.35)
        spacing = 48
        for i, opt in enumerate(self.options):
            color = (255, 255, 0) if i == self.index else (200, 200, 200)
            surf = self.font_opt.render(opt, True, color)
            x = (w - surf.get_width()) // 2
            y = start_y + i * spacing
            self.screen.blit(surf, (x, y))
