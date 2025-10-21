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
ANCHO, ALTO = 600, 600
TAM_CELDA = 40
RANGO = 10
DURACION_POWERUP = 300
ARCHIVO_PUNTUACIONES = "puntuaciones.json"
ARCHIVO_PERFILES = "perfiles.json"
ARCHIVO_CONFIG = "config.json"
ARCHIVO_NIVELES = "niveles.json"

# Carga niveles desde JSON
with open(ARCHIVO_NIVELES, "r") as f:
    datos_niveles = json.load(f)
NIVELES = datos_niveles["niveles"]

# Estado global
nivel_actual = 0
LABERINTO = NIVELES[0]["laberinto"]
FRAME_ENE = NIVELES[0]["vel_enemigos"]
pos_x, pos_y = 1, 1
estrellas, enemigos, powerups = [], [], []
vidas, puntuacion, contador_frames, powerup_timer = 3, 0, 0, 0
powerup_activo = None
puntuacion_final = 0
estado = "MENU"
perfil_actual = ""
nuevo_perfil = ""
creando_perfil = False
seleccionando_perfil = False
indice_perfil = 0
creando_contrasena = False
autenticando = False
modo_borrar = ""
nueva_contrasena = ""
contrasena_input = ""
mensaje_error = ""
tiempo_mensaje = 0

# Utilidades I/O
def cargar_json(path):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def cargar_perfiles():
    return cargar_json(ARCHIVO_PERFILES)

def cargar_puntuaciones():
    return cargar_json(ARCHIVO_PUNTUACIONES)

def cargar_config():
    if not os.path.exists(ARCHIVO_CONFIG):
        return {}
    try:
        with open(ARCHIVO_CONFIG, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def nombre_existe(n):
    return n.upper() in [p.upper() for p in cargar_perfiles()]

def guardar_perfil(n):
    perf = cargar_perfiles()
    if n.upper() in [p.upper() for p in perf]:
        return False
    perf.append(n)
    guardar_json(ARCHIVO_PERFILES, perf)
    return True

def guardar_puntuacion(n, p):
    pts = cargar_puntuaciones() + [{"nombre": n, "puntuacion": p}]
    pts = sorted(pts, key=lambda x: x["puntuacion"], reverse=True)[:10]
    guardar_json(ARCHIVO_PUNTUACIONES, pts)

def guardar_config(cfg):
    guardar_json(ARCHIVO_CONFIG, cfg)

def borrar_salon():
    open(ARCHIVO_PUNTUACIONES, "w").close()

def borrar_perfiles():
    open(ARCHIVO_PERFILES, "w").close()

# Generación de posiciones
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
    estrellas = generar_posiciones_validas(LAB, lvl["estrellas"], [(1, 1)])
    enemigos = generar_posiciones_validas(LAB, lvl["enemigos"], [(1, 1)] + estrellas)
    powerups = generar_posiciones_validas(LAB, lvl["powerups"], [(1, 1)] + estrellas + enemigos)
    vidas, puntuacion, contador_frames = 3, 0, 0
    powerup_activo, powerup_timer = None, 0

def avanzar_nivel():
    global nivel_actual, LABERINTO, FRAME_ENE
    if nivel_actual < len(NIVELES) - 1:
        nivel_actual += 1
        lvl = NIVELES[nivel_actual]
        LABERINTO = lvl["laberinto"]
        FRAME_ENE = lvl["vel_enemigos"]
        reiniciar_juego()
    else:
        evento_mgr.publicar(EventoGameOver(puntuacion))

reiniciar_juego()

# Inicialización Pygame
pygame.init()
reloj = pygame.time.Clock()
vista = Vista(ANCHO, ALTO, f"Maze-Run - Nivel {nivel_actual+1}")
evento_mgr = AdministradorDeEventos()
menu = MenuPrincipal(vista, evento_mgr)

# Controladores (omito para brevedad; copiar de tu versión anterior)
# ControladorJugador, ManejadorPowerUps, ControladorEnemigos, ManejadorColisiones, ManejadorEstrellas, ManejadorMenu

while True:
    # Actualizar mensaje temporal
    if tiempo_mensaje > 0:
        tiempo_mensaje -= 1
        if tiempo_mensaje <= 0:
            mensaje_error = ""

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Manejo de eventos por estado
        if estado == "MENU":
            menu.manejar_eventos(ev)

        elif estado == "JUEGO" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                estado = "MENU"
            # movimiento...

        elif estado == "GAME_OVER" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_RETURN:
                reiniciar_juego()
                estado = "JUEGO"
            elif ev.key == pygame.K_ESCAPE:
                estado = "MENU"

        elif estado == "SALON_FAMA" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                estado = "MENU"

        elif estado == "ADMINISTRACION" and ev.type == pygame.KEYDOWN:
            # Aquí toda la lógica de creación/perfil/contraseña/borrado
            # (copiar exactamente desde el bloque anterior)
            pass

    # Dibujo según estado
    if estado == "MENU":
        menu.dibujar()
        vista.actualizar()

    elif estado == "JUEGO":
        # Lógica y dibujo de juego
        vista.limpiar_pantalla((0,0,0))
        vista.dibujar_laberinto(LABERINTO, TAM_CELDA)
        # dibujar enemigos, estrellas, powerups, jugador, HUD...
        vista.actualizar()

    elif estado == "GAME_OVER":
        vista.limpiar_pantalla((50,0,0))
        vista.dibujar_texto("GAME OVER", 180,200,64,(255,0,0))
        vista.dibujar_texto(f"Punt.Fin:{puntuacion_final}",150,280,36,(255,255,255))
        vista.dibujar_texto("ENTER reint.",100,350,28,(200,200,200))
        vista.dibujar_texto("ESC menu",90,390,28,(200,200,200))
        vista.actualizar()

    elif estado == "SALON_FAMA":
        vista.limpiar_pantalla((0,0,50))
        vista.dibujar_texto("Salón De La Fama", 120,50,48,(255,255,0))
        y = 120
        for i,p in enumerate(cargar_puntuaciones()[:10]):
            vista.dibujar_texto(f"{i+1}. {p['nombre']}: {p['puntuacion']}",150,y,28,(255,255,255))
            y += 35
        vista.dibujar_texto("ESC volver",180,550,28,(200,200,200))
        vista.actualizar()

    elif estado == "ADMINISTRACION":
        vista.limpiar_pantalla((50,0,50))
        vista.dibujar_texto("Administración",150,50,48,(255,255,0))
        vista.dibujar_texto(f"Jugadores: {len(cargar_perfiles())}",150,90,24,(200,200,200))
        # Mostrar menús de creación, selección, contraseña, borrado
        # (copiar textos y cajas de tu versión previa)
        vista.actualizar()

    reloj.tick(60)
