import sys
import pygame
import json
import os
import random
from evento import (
    EventoMoverJugador, EventoSeleccionMenu, EventoColisionEnemigo,
    EventoRecogerEstrella, EventoPotenciadorRecogido, AdministradorEventos
)
from vista import Vista
from menu import MenuPrincipal
from pathfinding import encontrar_siguiente_paso_bfs as bfs_siguiente_paso
from constantes import (
    COLOR_FONDO, COLOR_TEXTO, COLOR_TEXTO_DESTACADO,
    COLOR_PARED_DEFAULT, COLOR_SUELO_DEFAULT,
    PUNTOS_POR_ESTRELLA, VIDAS_INICIALES, TAMAÑO_CELDA,
    POTENCIADOR_INVULNERABLE, POTENCIADOR_CONGELAR, POTENCIADOR_INVISIBLE,
    ESTADO_MENU, ESTADO_JUEGO, ESTADO_GAME_OVER, ESTADO_SALON, ESTADO_ADMIN,
)


class Juego:
    def __init__(self, ancho=900, alto=700, fps=50, ruta_niveles="niveles.json"):
        self.ancho, self.alto = ancho, alto
        self.fps = fps
        self.duracion_potenciador = 300
        self.ruta_niveles = ruta_niveles

        self.niveles = self._cargar_niveles()
        self.nivel_actual = 0
        if not self.niveles:
            self.niveles = [self._crear_nivel_emergencia()]
            self.sin_niveles_cargados = True
        else:
            self.sin_niveles_cargados = False

        self.laberinto = self.niveles[0]["laberinto"]
        self.laberinto = [[0 if c in (2, 3) else c for c in fila] for fila in self.laberinto]
        self.velocidad_enemigos = max(10, self.niveles[0].get("vel_enemigos", 14))
        self.tamano_celda = TAMAÑO_CELDA

        self.posicion_x = 1
        self.posicion_y = 1
        self.estrellas = []
        self.enemigos = []
        self.potenciadores = []
        self.vidas = VIDAS_INICIALES
        self.puntuacion = 0
        self.contador_cuadros = 0
        self.temporizador_potenciador = 0
        self.potenciador_activo = None
        self.puntuacion_final = 0
        self.estado = ESTADO_MENU
        self.mensaje_texto = ""
        self.cuadros_mensaje = 0
        self.retraso_paso_jugador = 7
        self.temporizador_paso_jugador = 0
        self.direcciones_presionadas = set()

        pygame.init()
        self.reloj = pygame.time.Clock()
        self.vista = Vista(self.ancho, self.alto, f"Maze-Run - Nivel {self.nivel_actual + 1}")
        self.administrador_eventos = AdministradorEventos()
        self.menu = MenuPrincipal(self.vista, self.administrador_eventos)
        self._registrar_manejadores()
        self._configurar_tablero()
        self._reiniciar_juego()

    # ... resto del archivo permanece igual, solo reemplazos de strings por constantes de estado ...
    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if self.estado == ESTADO_MENU:
                    self.menu.manejar_eventos(evento)
                elif self.estado == ESTADO_JUEGO:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = ESTADO_MENU
                        elif evento.key == pygame.K_UP:
                            self.direcciones_presionadas.add('arriba')
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_DOWN:
                            self.direcciones_presionadas.add('abajo')
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_LEFT:
                            self.direcciones_presionadas.add('izquierda')
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_RIGHT:
                            self.direcciones_presionadas.add('derecha')
                            self.temporizador_paso_jugador = 0
                    elif evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_UP:
                            self.direcciones_presionadas.discard('arriba')
                        elif evento.key == pygame.K_DOWN:
                            self.direcciones_presionadas.discard('abajo')
                        elif evento.key == pygame.K_LEFT:
                            self.direcciones_presionadas.discard('izquierda')
                        elif evento.key == pygame.K_RIGHT:
                            self.direcciones_presionadas.discard('derecha')
                elif self.estado == ESTADO_GAME_OVER:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = ESTADO_MENU
                        elif evento.key == pygame.K_RETURN and not self.sin_niveles_cargados:
                            self.nivel_actual = 0
                            self._reiniciar_juego()
                            self.estado = ESTADO_JUEGO
                elif self.estado == ESTADO_SALON:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.estado = ESTADO_MENU

            if self.estado == ESTADO_JUEGO:
                # ... sin cambios de lógica, omito por brevedad ...
                pass
            elif self.estado == ESTADO_MENU:
                self.menu.dibujar()
                self.vista.actualizar()
            elif self.estado == ESTADO_GAME_OVER:
                self.vista.limpiar_pantalla((30, 0, 0))
                self.vista.dibujar_texto("GAME OVER", 220, 200, 72, (255, 80, 80))
                self.vista.dibujar_texto(f"Puntaje final: {self.puntuacion_final}", 200, 280, 36, (255, 255, 255))
                self.vista.dibujar_texto("ENTER: Reintentar    ESC: Menú", 160, 340, 28, (220, 220, 220))
                self.vista.actualizar()
            elif self.estado == ESTADO_SALON:
                self.vista.limpiar_pantalla((0, 0, 50))
                self.vista.dibujar_texto("Salón de la Fama", 150, 200, 48, (255, 255, 0))
                puntuaciones = self._cargar_json("puntuaciones.json", [])
                y_posicion = 270
                for indice, entrada in enumerate(puntuaciones[:10]):
                    if isinstance(entrada, dict) and 'nombre' in entrada and 'puntuacion' in entrada:
                        self.vista.dibujar_texto(f"{indice + 1}. {entrada['nombre']}: {entrada['puntuacion']}", 120, y_posicion, 24, (255, 255, 255))
                        y_posicion += 30
                self.vista.dibujar_texto("ESC: Volver", 120, 550, 32, (200, 200, 200))
                self.vista.actualizar()
            elif self.estado == ESTADO_ADMIN:
                self.vista.limpiar_pantalla((50, 0, 0))
                self.vista.dibujar_texto("Administración", 180, 250, 48, (255, 255, 0))
                self.vista.dibujar_texto("ESC: Volver", 120, 350, 32, (200, 200, 200))
                self._recargar_niveles()
                self.estado = ESTADO_MENU
                self.vista.actualizar()

            self.reloj.tick(self.fps)
