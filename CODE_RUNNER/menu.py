

import pygame
from evento import EventoSeleccionMenu

class MenuPrincipal:
    def __init__(self, vista, evento_mgr):
        self.vista = vista
        self.evento_mgr = evento_mgr
        self.opciones = ["JUEGO", "SALON_FAMA", "ADMINISTRACION", "SALIR"]
        self.indice = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)

    def manejar_eventos(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_UP:
                self.indice = (self.indice - 1) % len(self.opciones)
            elif e.key == pygame.K_DOWN:
                self.indice = (self.indice + 1) % len(self.opciones)
            elif e.key == pygame.K_RETURN:
                opcion = self.opciones[self.indice]
                self.evento_mgr.publicar(EventoSeleccionMenu(opcion))

    def dibujar(self):
        # Fondo
        self.vista.limpiar_pantalla((0, 0, 0))

        # Título
        titulo_surf = self.fuente_titulo.render("Maze-Run", True, (255, 255, 255))
        x_titulo = (self.vista.ancho - titulo_surf.get_width()) // 2
        self.vista.pantalla.blit(titulo_surf, (x_titulo, 100))

        # Opciones
        for i, opcion in enumerate(self.opciones):
            color = (255, 255, 0) if i == self.indice else (200, 200, 200)
            surf = self.fuente_opcion.render(opcion, True, color)
            x_op = (self.vista.ancho - surf.get_width()) // 2
            y_op = 200 + i * 50
            self.vista.pantalla.blit(surf, (x_op, y_op))
