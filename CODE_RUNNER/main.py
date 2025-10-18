# main.py

import pygame
import random
from evento import (
    EventoMoverJugador,
    EventoSalir,
    EventoRecogerEstrella,
    EventoColisionEnemigo,
    AdministradorDeEventos
)
from vista import Vista

# --- Configuración ---
ANCHO, ALTO = 600, 600
TAM_CELDA = 40

LABERINTO = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,1,1,1,1,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Posiciones en celdas
pos_x, pos_y = 1, 1
estrellas = [(3,1), (10,2), (6,3)]
enemigos = [(5,1), (8,2)]
puntuacion = 0
vidas = 3

# Control de frames para enemigos
contador_frames = 0
FRAME_MOV_ENEMIGO = 30  # mover cada 30 iteraciones

# --- Inicialización ---
pygame.init()
reloj = pygame.time.Clock()
vista = Vista(ANCHO, ALTO, titulo="Laberinto Modular")
evento_mgr = AdministradorDeEventos()

# Controlador de jugador
class ControladorJugador:
    def __init__(self, evento_mgr):
        self.evento_mgr = evento_mgr
        evento_mgr.registrar(EventoMoverJugador, self)

    def notificar(self, evento):
        global pos_x, pos_y
        if isinstance(evento, EventoMoverJugador):
            dx = dy = 0
            if evento.direccion == 'arriba':     dy = -1
            elif evento.direccion == 'abajo':    dy = 1
            elif evento.direccion == 'izquierda': dx = -1
            elif evento.direccion == 'derecha':   dx = 1
            nx, ny = pos_x + dx, pos_y + dy
            if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0:
                pos_x, pos_y = nx, ny

ControladorJugador(evento_mgr)

# Manejador de estrellas
class ManejadorEstrellas:
    def __init__(self, evento_mgr):
        evento_mgr.registrar(EventoRecogerEstrella, self)

    def notificar(self, evento):
        global puntuacion, estrellas
        if isinstance(evento, EventoRecogerEstrella):
            if evento.posicion in estrellas:
                estrellas.remove(evento.posicion)
                puntuacion += 10

ManejadorEstrellas(evento_mgr)

# Controlador de enemigos
class ControladorEnemigos:
    def __init__(self, evento_mgr):
        self.evento_mgr = evento_mgr

    def actualizar(self):
        global enemigos, contador_frames, pos_x, pos_y
        contador_frames += 1
        if contador_frames < FRAME_MOV_ENEMIGO:
            return
        contador_frames = 0

        nuevos = []
        for ex, ey in enemigos:
            dx, dy = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            nx, ny = ex + dx, ey + dy
            if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0:
                ex, ey = nx, ny
            if (ex, ey) == (pos_x, pos_y):
                self.evento_mgr.publicar(EventoColisionEnemigo((pos_x, pos_y), (ex, ey)))
            nuevos.append((ex, ey))
        enemigos = nuevos

controlador_enemigos = ControladorEnemigos(evento_mgr)

# Manejador de colisiones con enemigos
class ManejadorColisiones:
    def __init__(self, evento_mgr):
        evento_mgr.registrar(EventoColisionEnemigo, self)

    def notificar(self, evento):
        global vidas, pos_x, pos_y
        if isinstance(evento, EventoColisionEnemigo):
            vidas -= 1
            pos_x, pos_y = 1, 1

ManejadorColisiones(evento_mgr)

# --- Bucle Principal ---
corriendo = True
while corriendo:
    # 1. Eventos de pygame → eventos del juego
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            evento_mgr.publicar(EventoSalir())
            corriendo = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                evento_mgr.publicar(EventoSalir())
                corriendo = False
            elif e.key == pygame.K_UP:
                evento_mgr.publicar(EventoMoverJugador('arriba'))
            elif e.key == pygame.K_DOWN:
                evento_mgr.publicar(EventoMoverJugador('abajo'))
            elif e.key == pygame.K_LEFT:
                evento_mgr.publicar(EventoMoverJugador('izquierda'))
            elif e.key == pygame.K_RIGHT:
                evento_mgr.publicar(EventoMoverJugador('derecha'))

    # 2. Recolección de estrellas
    pos_jugador = (pos_x, pos_y)
    if pos_jugador in estrellas:
        evento_mgr.publicar(EventoRecogerEstrella(pos_jugador))

    # 3. Movimiento de enemigos y detección de colisión
    controlador_enemigos.actualizar()

    # 4. Renderizado
    vista.limpiar_pantalla((0, 0, 0))
    vista.dibujar_laberinto(LABERINTO, TAM_CELDA)
    for ex, ey in enemigos:
        vista.dibujar_enemigo(ex * TAM_CELDA, ey * TAM_CELDA, TAM_CELDA)
    for ex, ey in estrellas:
        vista.dibujar_estrella(ex * TAM_CELDA, ey * TAM_CELDA, TAM_CELDA)
    vista.dibujar_jugador(pos_x * TAM_CELDA, pos_y * TAM_CELDA, TAM_CELDA)
    vista.dibujar_hud(vidas, puntuacion)
    vista.actualizar()

    # 5. Control de FPS
    reloj.tick(60)

pygame.quit()
