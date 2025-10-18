# main.py

import pygame
import random
from evento import (
    EventoMoverJugador,
    EventoSalir,
    EventoRecogerEstrella,
    EventoColisionEnemigo,
    EventoSeleccionMenu,
    EventoGameOver,
    AdministradorDeEventos
)
from vista import Vista
from menu import MenuPrincipal
from pathfinding import bfs_siguiente_paso, distancia_manhattan

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

def generar_posiciones_validas(laberinto, cantidad, excluir):
    posiciones, filas, cols = [], len(laberinto), len(laberinto[0])
    intentos, max_int = 0, cantidad * 50
    while len(posiciones) < cantidad and intentos < max_int:
        x, y = random.randint(1, cols-2), random.randint(1, filas-2)
        if laberinto[y][x] == 0 and (x,y) not in excluir and (x,y) not in posiciones:
            posiciones.append((x,y))
        intentos += 1
    return posiciones

def reiniciar_juego():
    global pos_x, pos_y, estrellas, enemigos, puntuacion, vidas, contador_frames
    pos_x, pos_y = 1, 1
    estrellas = generar_posiciones_validas(LABERINTO, 3, [(pos_x, pos_y)])
    enemigos = generar_posiciones_validas(LABERINTO, 2, [(pos_x, pos_y)] + estrellas)
    puntuacion = 0
    vidas = 3
    contador_frames = 0

# Variables globales
pos_x, pos_y = 1, 1
estrellas, enemigos = [], []
puntuacion, vidas, contador_frames = 0, 3, 0
FRAME_ENE, RANGO = 15, 7
puntuacion_final = 0

reiniciar_juego()

pygame.init()
reloj = pygame.time.Clock()
vista = Vista(ANCHO, ALTO, "Maze-Run")
evento_mgr = AdministradorDeEventos()

estado = "MENU"
menu = MenuPrincipal(vista, evento_mgr)

class ControladorJugador:
    def __init__(self, mgr): mgr.registrar(EventoMoverJugador, self)
    def notificar(self, e):
        global pos_x, pos_y
        if isinstance(e, EventoMoverJugador) and vidas > 0:
            dx = dy = 0
            if e.direccion == 'arriba': dy = -1
            elif e.direccion == 'abajo': dy = 1
            elif e.direccion == 'izquierda': dx = -1
            elif e.direccion == 'derecha': dx = 1
            nx, ny = pos_x + dx, pos_y + dy
            if LABERINTO[ny][nx] == 0:
                pos_x, pos_y = nx, ny

class ManejadorEstrellas:
    def __init__(self, mgr): mgr.registrar(EventoRecogerEstrella, self)
    def notificar(self, e):
        global puntuacion
        if isinstance(e, EventoRecogerEstrella) and e.posicion in estrellas:
            estrellas.remove(e.posicion)
            puntuacion += 10

class ControladorEnemigos:
    def __init__(self, mgr): self.mgr = mgr
    def actualizar(self):
        global enemigos, contador_frames
        if vidas <= 0: return
        contador_frames += 1
        if contador_frames < FRAME_ENE: return
        contador_frames = 0

        nuevos = []
        ocup = set()
        for ex, ey in enemigos:
            dist = distancia_manhattan((ex, ey), (pos_x, pos_y))
            nuevo = None
            if dist <= RANGO:
                paso = bfs_siguiente_paso(LABERINTO, (ex, ey), (pos_x, pos_y))
                if paso and paso not in ocup:
                    nuevo = paso
            if not nuevo:
                dirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = ex+dx, ey+dy
                    if (0 <= nx < len(LABERINTO[0]) and 0 <= ny < len(LABERINTO) and
                        LABERINTO[ny][nx] == 0 and (nx, ny) not in ocup):
                        nuevo = (nx, ny)
                        break
            if not nuevo: nuevo = (ex, ey)
            ex, ey = nuevo
            if (ex, ey) == (pos_x, pos_y):
                self.mgr.publicar(EventoColisionEnemigo((pos_x, pos_y), (ex, ey)))
            ocup.add((ex, ey))
            nuevos.append((ex, ey))
        enemigos = nuevos

class ManejadorColisiones:
    def __init__(self, mgr):
        self.mgr = mgr
        mgr.registrar(EventoColisionEnemigo, self)
        self.last = -100
    def notificar(self, e):
        global vidas, pos_x, pos_y, puntuacion_final
        if isinstance(e, EventoColisionEnemigo):
            if contador_frames - self.last < 30: return
            self.last = contador_frames
            vidas -= 1
            if vidas > 0:
                pos_x, pos_y = 1, 1
            else:
                puntuacion_final = puntuacion
                self.mgr.publicar(EventoGameOver(puntuacion_final))

class ManejadorMenu:
    def __init__(self, mgr): mgr.registrar(EventoSeleccionMenu, self)
    def notificar(self, e):
        global estado
        if isinstance(e, EventoSeleccionMenu):
            if e.opcion == "JUEGO": reiniciar_juego()
            estado = e.opcion

class ManejadorGameOver:
    def __init__(self, mgr): mgr.registrar(EventoGameOver, self)
    def notificar(self, e):
        global estado
        if isinstance(e, EventoGameOver):
            estado = "GAME_OVER"

ControladorJugador(evento_mgr)
ManejadorEstrellas(evento_mgr)
controlador_enemigos = ControladorEnemigos(evento_mgr)
ManejadorColisiones(evento_mgr)
ManejadorMenu(evento_mgr)
ManejadorGameOver(evento_mgr)

while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()
        if estado == "MENU":
            menu.manejar_eventos(ev)
        elif estado == "JUEGO" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                estado = "MENU"
            elif ev.key == pygame.K_UP:
                evento_mgr.publicar(EventoMoverJugador('arriba'))
            elif ev.key == pygame.K_DOWN:
                evento_mgr.publicar(EventoMoverJugador('abajo'))
            elif ev.key == pygame.K_LEFT:
                evento_mgr.publicar(EventoMoverJugador('izquierda'))
            elif ev.key == pygame.K_RIGHT:
                evento_mgr.publicar(EventoMoverJugador('derecha'))
        elif estado == "GAME_OVER" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                reiniciar_juego()
                estado = "JUEGO"
            elif ev.key == pygame.K_ESCAPE:
                estado = "MENU"
        elif estado in ("SALON_FAMA", "ADMINISTRACION") and ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            estado = "MENU"

    if estado == "MENU":
        menu.dibujar()
        vista.actualizar()

    elif estado == "JUEGO":
        if vidas > 0 and (pos_x, pos_y) in estrellas:
            evento_mgr.publicar(EventoRecogerEstrella((pos_x, pos_y)))

        controlador_enemigos.actualizar()

        vista.limpiar_pantalla((0, 0, 0))
        vista.dibujar_laberinto(LABERINTO, TAM_CELDA)
        for ex, ey in enemigos:
            vista.dibujar_enemigo(ex * TAM_CELDA, ey * TAM_CELDA, TAM_CELDA)
        for sx, sy in estrellas:
            vista.dibujar_estrella(sx * TAM_CELDA, sy * TAM_CELDA, TAM_CELDA)
        vista.dibujar_jugador(pos_x * TAM_CELDA, pos_y * TAM_CELDA, TAM_CELDA)
        vista.dibujar_hud(vidas, puntuacion)
        vista.actualizar()

    elif estado == "GAME_OVER":
        vista.limpiar_pantalla((50, 0, 0))
        vista.dibujar_texto("GAME OVER", 180, 200, 64, (255, 0, 0))
        vista.dibujar_texto(f"Puntuación Final: {puntuacion_final}", 150, 280, 36, (255, 255, 255))
        vista.dibujar_texto("ENTER para reintentar", 100, 350, 28, (200, 200, 200))
        vista.dibujar_texto("ESC para menú", 90, 390, 28, (200, 200, 200))
        vista.actualizar()

    elif estado == "SALON_FAMA":
        vista.limpiar_pantalla((0, 0, 50))
        vista.dibujar_texto("Salón de la Fama", 150, 250, 48, (255, 255, 0))
        vista.dibujar_texto("ESC para volver", 120, 350, 32)
        vista.actualizar()

    elif estado == "ADMINISTRACION":
        vista.limpiar_pantalla((50, 0, 0))
        vista.dibujar_texto("Administración", 180, 250, 48, (255, 255, 0))
        vista.dibujar_texto("ESC para volver", 120, 350, 32)
        vista.actualizar()

    reloj.tick(60)

