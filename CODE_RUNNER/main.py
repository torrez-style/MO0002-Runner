

import pygame
import random
from evento import (
    EventoMoverJugador,
    EventoSalir,
    EventoRecogerEstrella,
    EventoColisionEnemigo,
    EventoSeleccionMenu,
    AdministradorDeEventos
)
from vista import Vista
from menu import MenuPrincipal

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

# Variables globales del juego
pos_x, pos_y = 1, 1
estrellas = [(3,1), (10,2), (6,3)]
enemigos = [(5,1), (8,2)]
puntuacion = 0
vidas = 3
contador_frames = 0
FRAME_MOV_ENEMIGO = 30

# --- Inicialización ---
pygame.init()
reloj = pygame.time.Clock()
vista = Vista(ANCHO, ALTO, titulo="Maze-Run")
evento_mgr = AdministradorDeEventos()

# Estado inicial
estado = "MENU"
menu = MenuPrincipal(vista, evento_mgr)

# --- Controladores y Manejadores ---
class ControladorJugador:
    def __init__(self, evento_mgr):
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

class ManejadorEstrellas:
    def __init__(self, evento_mgr):
        evento_mgr.registrar(EventoRecogerEstrella, self)

    def notificar(self, evento):
        global puntuacion, estrellas
        if isinstance(evento, EventoRecogerEstrella):
            if evento.posicion in estrellas:
                estrellas.remove(evento.posicion)
                puntuacion += 10

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

class ManejadorColisiones:
    def __init__(self, evento_mgr):
        evento_mgr.registrar(EventoColisionEnemigo, self)

    def notificar(self, evento):
        global vidas, pos_x, pos_y
        if isinstance(evento, EventoColisionEnemigo):
            vidas -= 1
            pos_x, pos_y = 1, 1

class ManejadorMenu:
    def __init__(self, evento_mgr):
        evento_mgr.registrar(EventoSeleccionMenu, self)

    def notificar(self, evento):
        global estado
        if isinstance(evento, EventoSeleccionMenu):
            estado = evento.opcion

# Instanciar controladores
controlador_jugador = ControladorJugador(evento_mgr)
manejador_estrellas = ManejadorEstrellas(evento_mgr)
controlador_enemigos = ControladorEnemigos(evento_mgr)
manejador_colisiones = ManejadorColisiones(evento_mgr)
manejador_menu = ManejadorMenu(evento_mgr)

# --- Bucle Principal ---
corriendo = True
while corriendo:
    # Manejo de eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            corriendo = False
        
        if estado == "MENU":
            menu.manejar_eventos(e)
        elif estado == "JUEGO":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    estado = "MENU"
                elif e.key == pygame.K_UP:
                    evento_mgr.publicar(EventoMoverJugador('arriba'))
                elif e.key == pygame.K_DOWN:
                    evento_mgr.publicar(EventoMoverJugador('abajo'))
                elif e.key == pygame.K_LEFT:
                    evento_mgr.publicar(EventoMoverJugador('izquierda'))
                elif e.key == pygame.K_RIGHT:
                    evento_mgr.publicar(EventoMoverJugador('derecha'))
    
    # Actualización según el estado
    if estado == "MENU":
        menu.dibujar()
        vista.actualizar()
    
    elif estado == "JUEGO":
        # Recolección de estrellas
        if (pos_x, pos_y) in estrellas:
            evento_mgr.publicar(EventoRecogerEstrella((pos_x, pos_y)))
        
        # Movimiento de enemigos
        controlador_enemigos.actualizar()
        
        # Renderizado
        vista.limpiar_pantalla((0, 0, 0))
        vista.dibujar_laberinto(LABERINTO, TAM_CELDA)
        for ex, ey in enemigos:
            vista.dibujar_enemigo(ex * TAM_CELDA, ey * TAM_CELDA, TAM_CELDA)
        for ex, ey in estrellas:
            vista.dibujar_estrella(ex * TAM_CELDA, ey * TAM_CELDA, TAM_CELDA)
        vista.dibujar_jugador(pos_x * TAM_CELDA, pos_y * TAM_CELDA, TAM_CELDA)
        vista.dibujar_hud(vidas, puntuacion)
        vista.actualizar()
    
    elif estado == "SALON_FAMA":
        # Placeholder para salón de la fama
        vista.limpiar_pantalla((0, 0, 50))
        vista.dibujar_texto("Salón de la Fama", 150, 250, 48, (255, 255, 0))
        vista.dibujar_texto("Presiona ESC para volver", 120, 350, 32)
        vista.actualizar()
    
    elif estado == "ADMINISTRACION":
        # Placeholder para administración
        vista.limpiar_pantalla((50, 0, 0))
        vista.dibujar_texto("Administración", 180, 250, 48, (255, 255, 0))
        vista.dibujar_texto("Presiona ESC para volver", 120, 350, 32)
        vista.actualizar()
    
    elif estado == "SALIR":
        corriendo = False
    
    reloj.tick(60)

pygame.quit()
