# menu.py

import pygame
from evento import EventoSeleccionMenu, EventoSalir

class MenuPrincipal:
    """Menú principal del juego"""
    
    def __init__(self, vista, evento_mgr):
        self.vista = vista
        self.evento_mgr = evento_mgr
        self.opciones = [
            "Iniciar juego",
            "Salón de la fama",
            "Administración",
            "Salir"
        ]
        self.indice_seleccion = 0
        self.COLOR_SELECCION = (255, 0, 0)  # Rojo
        self.COLOR_NORMAL = (255, 255, 255)  # Blanco
    
    def manejar_eventos(self, evento):
        """Maneja los eventos del teclado en el menú"""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_seleccion = (self.indice_seleccion - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.indice_seleccion = (self.indice_seleccion + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN or evento.key == pygame.K_SPACE:
                opcion_seleccionada = self.opciones[self.indice_seleccion]
                if opcion_seleccionada == "Iniciar juego":
                    self.evento_mgr.publicar(EventoSeleccionMenu("JUEGO"))
                elif opcion_seleccionada == "Salón de la fama":
                    self.evento_mgr.publicar(EventoSeleccionMenu("SALON_FAMA"))
                elif opcion_seleccionada == "Administración":
                    self.evento_mgr.publicar(EventoSeleccionMenu("ADMINISTRACION"))
                elif opcion_seleccionada == "Salir":
                    self.evento_mgr.publicar(EventoSalir())
    
    def dibujar(self):
        """Dibuja el menú en la pantalla"""
        self.vista.limpiar_pantalla((0, 0, 0))
        
        # Título del juego
        self.vista.dibujar_texto(
            "MAZE-RUN",
            self.vista.ancho_pantalla // 2 - 100,
            100,
            tamano_fuente=72,
            color=(255, 255, 0)
        )
        
        # Dibujar opciones
        y_inicial = 250
        espaciado = 60
        
        for i, opcion in enumerate(self.opciones):
            color = self.COLOR_SELECCION if i == self.indice_seleccion else self.COLOR_NORMAL
            x = self.vista.ancho_pantalla // 2 - 100
            y = y_inicial + (i * espaciado)
            self.vista.dibujar_texto(opcion, x, y, tamano_fuente=36, color=color)
        
        # Instrucciones
        self.vista.dibujar_texto(
            "Usa las flechas y Enter para seleccionar",
            self.vista.ancho_pantalla // 2 - 200,
            self.vista.alto_pantalla - 50,
            tamano_fuente=24,
            color=(200, 200, 200)
        )
