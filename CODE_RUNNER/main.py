import pygame
import random
import json
import os
from evento import (
    EventoMoverJugador, EventoSalir, EventoRecogerEstrella,
    EventoColisionEnemigo, EventoSeleccionMenu, EventoGameOver,
    EventoPowerUpAgarrado, AdministradorDeEventos
)
from vista import Vista
from menu import MenuPrincipal
from pathfinding import bfs_siguiente_paso, distancia_manhattan

# CONFIGURACIÓN
ANCHO, ALTO = 900, 700
FPS = 50
RANGO = 10
DURACION_POWERUP = 300
ARCHIVO_PUNTUACIONES = "puntuaciones.json"
ARCHIVO_PERFILES = "perfiles.json"
ARCHIVO_CONFIG = "config.json"
ARCHIVO_NIVELES = "niveles.json"

# Carga niveles
with open(ARCHIVO_NIVELES, "r", encoding="utf-8") as f:
    datos_niveles = json.load(f)
NIVELES = datos_niveles["niveles"]

# Estado
nivel_actual = 0
LABERINTO = NIVELES[0]["laberinto"]
FRAME_ENE = max(12, NIVELES[0]["vel_enemigos"])  # mínimo para que no sea tan rápido
TAM_CELDA = 40
pos_x, pos_y = 1, 1
estrellas, enemigos, powerups = [], [], []
vidas, puntuacion, contador_frames, powerup_timer = 3, 0, 0, 0
powerup_activo = None
puntuacion_final = 0
estado = "MENU"
perfil_actual = ""
mensaje_error = ""
tiempo_mensaje = 0

# Movimiento suave por pasos (tecla sostenida)
PLAYER_STEP_DELAY = 7   # frames entre pasos cuando está sostenida
PLAYER_TAP_DELAY = 2    # delay tras un toque
player_step_timer = 0
held_dirs = set()

# I/O

def cargar_json(path, default=None):
    if not os.path.exists(path):
        return default if default is not None else []
    try:
        with open(path, "r", encoding="utf-8") as f:
            txt = f.read().strip()
            return json.loads(txt) if txt else (default if default is not None else [])
    except json.JSONDecodeError:
        return default if default is not None else []

# Tablero dinámico

def configurar_tablero(vista, laberinto):
    global TAM_CELDA
    filas, cols = len(laberinto), len(laberinto[0])
    # AUMENTAR ÁREA JUGABLE para que el tablero se vea grande
    area_w, area_h = 800, 600
    TAM_CELDA = max(24, min(area_w // cols, area_h // filas))
    tablero_w = TAM_CELDA * cols
    tablero_h = TAM_CELDA * filas
    vista.offset_x = (vista.ancho - tablero_w) // 2
    vista.offset_y = (vista.alto - tablero_h) // 2 + 20

# Posiciones

def generar_posiciones_validas(lab, c, ex):
    pos = []
    filas, cols = len(lab), len(lab[0])
    i = 0
    while len(pos) < c and i < c * 50:
        x, y = random.randint(1, cols - 2), random.randint(1, filas - 2)
        if lab[y][x] == 0 and (x, y) not in ex + pos:
            pos.append((x, y))
        i += 1
    return pos

def jugador_celda_libre():
    libres = [
        (x, y)
        for y in range(1, len(LABERINTO) - 1)
        for x in range(1, len(LABERINTO[0]) - 1)
        if LABERINTO[y][x] == 0 and (x, y) not in enemigos
    ]
    return random.choice(libres) if libres else (1, 1)

def reiniciar_juego():
    global pos_x, pos_y, estrellas, enemigos, powerups, vidas, puntuacion, contador_frames, powerup_activo, powerup_timer
    lvl = NIVELES[nivel_actual]
    LAB = lvl["laberinto"]
    pos_x, pos_y = 1, 1
    estrellas = generar_posiciones_validas(LAB, lvl.get("estrellas", 3), [(1, 1)])
    enemigos = generar_posiciones_validas(LAB, lvl.get("enemigos", 2), [(1, 1)] + estrellas)
    powerups = generar_posiciones_validas(LAB, lvl.get("powerups", 2), [(1, 1)] + estrellas + enemigos)
    vidas, puntuacion, contador_frames = 3, 0, 0
    powerup_activo, powerup_timer = None, 0

def avanzar_nivel():
    global nivel_actual, LABERINTO, FRAME_ENE
    if nivel_actual < len(NIVELES) - 1:
        nivel_actual += 1
        lvl = NIVELES[nivel_actual]
        LABERINTO = lvl["laberinto"]
        FRAME_ENE = max(10, lvl.get("vel_enemigos", 12))
        configurar_tablero(vista, LABERINTO)
        reiniciar_juego()
    else:
        evento_mgr.publicar(EventoGameOver(puntuacion))

# Pygame
pygame.init()
reloj = pygame.time.Clock()
vista = Vista(ANCHO, ALTO, f"Maze-Run - Nivel {nivel_actual+1}")
from evento import AdministradorDeEventos
evento_mgr = AdministradorDeEventos()
menu = MenuPrincipal(vista, evento_mgr)
configurar_tablero(vista, LABERINTO)

# Controladores y resto del archivo continúa igual...
