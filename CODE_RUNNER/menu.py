import pygame
import os
import json
from evento import EventoSeleccionMenu
from salon_de_la_fama import SalonDeLaFama

class MenuPrincipal:
    ...
    def _dibujar_salon_fama(self):
        fondo = pygame.Surface((700, 450))
        fondo.fill((42, 42, 52))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho // 2, self.vista.alto // 2)
        self.vista.pantalla.blit(fondo, rect)
        fuente_titulo = pygame.font.SysFont(None, 40)
        fuente_texto = pygame.font.SysFont(None, 28)
        titulo = fuente_titulo.render("SALÓN DE LA FAMA", True, (255, 215, 0))
        self.vista.pantalla.blit(titulo, (rect.left + 150, rect.top + 20))
        ranking = self.salon.obtener_ranking_global()  # <---- sin argumento extra
        y_pos = rect.top + 70
        if ranking:
            for idx, entrada in enumerate(ranking, 1):
                texto = f"{idx}. {entrada['usuario']} - {entrada['puntuacion']} pts"
                surf = fuente_texto.render(texto, True, (200, 255, 200))
                self.vista.pantalla.blit(surf, (rect.left + 30, y_pos))
                y_pos += 30
        else:
            sin_datos = fuente_texto.render("Sin datos aún", True, (200, 200, 200))
            self.vista.pantalla.blit(sin_datos, (rect.left + 30, y_pos))
        instruccion = fuente_texto.render("ENTER/ESC: Volver", True, (180, 180, 180))
        self.vista.pantalla.blit(instruccion, (rect.left + 30, rect.bottom - 40))
    ...