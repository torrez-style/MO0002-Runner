import pygame
import json
import os
import random
from evento import (
    EventoMoverJugador,
    EventoSeleccionMenu,
    EventoColisionEnemigo,
    EventoRecogerEstrella,
    EventoPowerUpAgarrado,
    AdministradorDeEventos,
)
from vista import Vista
from menu import MenuPrincipal
from salon_de_la_fama import SalonDeLaFama
from pathfinding import bfs_siguiente_paso

class Juego:
    def __init__(self, ancho=900, alto=700, fps=50, ruta_niveles="niveles.json"):
        self.ANCHO, self.ALTO = ancho, alto
        self.FPS = fps
        self.DURACION_POTENCIADOR = 300
        self.ruta_niveles = ruta_niveles
        self.niveles = self._cargar_niveles()
        self.nivel_actual = 0
        if not self.niveles or len(self.niveles) == 0:
            self.niveles = [self._crear_nivel_emergencia()]
            self.sin_niveles_cargados = True
        else:
            self.sin_niveles_cargados = False
        self.LABERINTO = self.niveles[0]["laberinto"]
        self.LABERINTO = [
            [0 if c in (2, 3) else c for c in fila] for fila in self.LABERINTO
        ]
        self.VELOCIDAD_ENEMIGOS = max(10, self.niveles[0].get("vel_enemigos", 14))
        self.tamaño_celda = 32
        self.posicion_x = 1
        self.posicion_y = 1
        self.estrellas = []
        self.enemigos = []
        self.potenciadores = []
        self.vidas = 3
        self.puntuacion = 0
        self.contador_cuadros = 0
        self.temporizador_potenciador = 0
        self.potenciador_activo = None
        self.puntuacion_final = 0
        self.estado = "MENU"
        self.mensaje_texto = ""
        self.cuadros_mensaje = 0
        self.RETRASO_PASO_JUGADOR = 7
        self.temporizador_paso_jugador = 0
        self.direcciones_presionadas = set()
        pygame.init()
        self.reloj = pygame.time.Clock()
        self.vista = Vista(
            self.ANCHO, self.ALTO, f"Maze-Run - Nivel {self.nivel_actual + 1}"
        )
        self.administrador_eventos = AdministradorDeEventos()
        self.menu = MenuPrincipal(self.vista, self.administrador_eventos)
        self.salon = SalonDeLaFama()
        self.usuario_actual = None
        self._registrar_manejadores()
        self._configurar_tablero()
        self._reiniciar_juego()

    # ... (todo igual: clases, métodos, etc) ...
    # SOLO cambiar el bloque principal del método ejecutar()
    # EN VEZ de dibujar SIEMPRE el juego, hacer sólo si estado=='JUEGO':
    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if self.estado == "MENU":
                    self.menu.manejar_eventos(evento)
                elif self.estado == "JUEGO":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                        elif evento.key == pygame.K_UP:
                            self.direcciones_presionadas.add("arriba")
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_DOWN:
                            self.direcciones_presionadas.add("abajo")
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_LEFT:
                            self.direcciones_presionadas.add("izquierda")
                            self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_RIGHT:
                            self.direcciones_presionadas.add("derecha")
                            self.temporizador_paso_jugador = 0
                    elif evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_UP:
                            self.direcciones_presionadas.discard("arriba")
                        elif evento.key == pygame.K_DOWN:
                            self.direcciones_presionadas.discard("abajo")
                        elif evento.key == pygame.K_LEFT:
                            self.direcciones_presionadas.discard("izquierda")
                        elif evento.key == pygame.K_RIGHT:
                            self.direcciones_presionadas.discard("derecha")
                elif self.estado == "GAME_OVER":
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            self.estado = "MENU"
                        elif (
                            evento.key == pygame.K_RETURN
                            and not self.sin_niveles_cargados
                        ):
                            self.nivel_actual = 0
                            self._reiniciar_juego()
                            self.estado = "JUEGO"
                elif self.estado == "SALÓN_DE_LA_FAMA":
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                        self.estado = "MENU"
            # SOLO actualizar y dibujar si el estado es JUEGO
            if self.estado == "JUEGO":
                if self.direcciones_presionadas:
                    self.temporizador_paso_jugador -= 1
                    if self.temporizador_paso_jugador <= 0:
                        if "arriba" in self.direcciones_presionadas:
                            self.administrador_eventos.publicar(
                                EventoMoverJugador("arriba")
                            )
                        elif "abajo" in self.direcciones_presionadas:
                            self.administrador_eventos.publicar(
                                EventoMoverJugador("abajo")
                            )
                        elif "izquierda" in self.direcciones_presionadas:
                            self.administrador_eventos.publicar(
                                EventoMoverJugador("izquierda")
                            )
                        elif "derecha" in self.direcciones_presionadas:
                            self.administrador_eventos.publicar(
                                EventoMoverJugador("derecha")
                            )
                        self.temporizador_paso_jugador = self.RETRASO_PASO_JUGADOR
                if (
                    self.vidas > 0
                    and (self.posicion_x, self.posicion_y) in self.estrellas
                ):
                    self.administrador_eventos.publicar(
                        EventoRecogerEstrella((self.posicion_x, self.posicion_y))
                    )
                if (
                    self.vidas > 0
                    and (self.posicion_x, self.posicion_y) in self.potenciadores
                ):
                    self.potenciadores.remove((self.posicion_x, self.posicion_y))
                    self.administrador_eventos.publicar(
                        EventoPowerUpAgarrado(
                            random.choice(["invulnerable", "congelar", "invisible"])
                        )
                    )
                if self.cuadros_mensaje > 0:
                    self.cuadros_mensaje -= 1
                self.controlador_enemigos.actualizar()
                self.vista.limpiar_pantalla((0, 0, 0))
                nivel_actual = self.niveles[self.nivel_actual]
                color_pared = tuple(
                    nivel_actual.get("colores", {}).get("pared", (80, 80, 80))
                )
                color_suelo = tuple(
                    nivel_actual.get("colores", {}).get("suelo", (220, 230, 245))
                )
                color_enemigo = tuple(
                    nivel_actual.get("colores", {}).get("enemigo", (220, 50, 50))
                )
                self.vista.dibujar_laberinto(
                    self.LABERINTO, self.tamaño_celda, color_pared, color_suelo
                )
                for enemigo_x, enemigo_y in self.enemigos:
                    self.vista.dibujar_enemigo(
                        enemigo_x * self.tamaño_celda,
                        enemigo_y * self.tamaño_celda,
                        self.tamaño_celda,
                        color=color_enemigo,
                    )
                for estrella_x, estrella_y in self.estrellas:
                    self.vista.dibujar_estrella(
                        estrella_x * self.tamaño_celda,
                        estrella_y * self.tamaño_celda,
                        self.tamaño_celda,
                    )
                for potenciador_x, potenciador_y in self.potenciadores:
                    self.vista.dibujar_potenciador(
                        potenciador_x * self.tamaño_celda,
                        potenciador_y * self.tamaño_celda,
                        self.tamaño_celda,
                    )
                self.vista.dibujar_jugador(
                    self.posicion_x * self.tamaño_celda,
                    self.posicion_y * self.tamaño_celda,
                    self.tamaño_celda,
                )
                self.vista.dibujar_texto(
                    f"Estrellas restantes: {len(self.estrellas)}", 20, 20, 24, (255, 255, 0)
                )
                self.vista.dibujar_interfaz(
                    self.vidas, self.puntuacion, x=20, y=self.desplazamiento_interfaz_y
                )
                if self.mensaje_texto and self.cuadros_mensaje > 0:
                    self.vista.dibujar_texto(self.mensaje_texto, 120, 60, 32, (255, 64, 64))
                self.vista.actualizar()
            elif self.estado == "MENU":
                self.vista.limpiar_pantalla((0, 0, 0))
                self.menu.dibujar()
                self.vista.actualizar()
            elif self.estado == "GAME_OVER":
                self.vista.limpiar_pantalla((30, 0, 0))
                self.vista.dibujar_texto("GAME OVER", 220, 200, 72, (255, 80, 80))
                self.vista.dibujar_texto(
                    f"Puntaje final: {self.puntuacion_final}",
                    200,
                    280,
                    36,
                    (255, 255, 255),
                )
                self.vista.dibujar_texto(
                    "ENTER: Reintentar ESC: Menú", 160, 340, 28, (220, 220, 220)
                )
                self.vista.actualizar()
            elif self.estado == "SALÓN_DE_LA_FAMA":
                self.vista.limpiar_pantalla((0, 0, 50))
                self.vista.dibujar_texto(
                    "Salón de la Fama", 150, 200, 48, (255, 255, 0)
                )
                puntuaciones = self._cargar_json("puntuaciones.json", {})
                y_posicion = 270
                if isinstance(puntuaciones, dict):
                    for usuario, scores in list(puntuaciones.items())[:10]:
                        if scores and isinstance(scores, list):
                            mejor_score = max(
                                [
                                    s.get("puntuacion", 0)
                                    for s in scores
                                    if isinstance(s, dict)
                                ],
                                default=0,
                            )
                            self.vista.dibujar_texto(
                                f"{usuario}: {mejor_score}",
                                120,
                                y_posicion,
                                24,
                                (255, 255, 255),
                            )
                            y_posicion += 30
                self.vista.dibujar_texto("ESC: Volver", 120, 550, 32, (200, 200, 200))
                self.vista.actualizar()
            self.reloj.tick(self.FPS)
