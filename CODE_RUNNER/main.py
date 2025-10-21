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
PLAYER_STEP_DELAY = 7
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
evento_mgr = AdministradorDeEventos()
menu = MenuPrincipal(vista, evento_mgr)
configurar_tablero(vista, LABERINTO)

# Controladores
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
            if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0:
                pos_x, pos_y = nx, ny

class ManejadorPowerUps:
    def __init__(self, mgr): mgr.registrar(EventoPowerUpAgarrado, self)
    def notificar(self, e):
        global powerup_activo, powerup_timer
        powerup_activo = e.tipo
        powerup_timer = DURACION_POWERUP

class ControladorEnemigos:
    def __init__(self, mgr): self.mgr = mgr
    def actualizar(self):
        global enemigos, contador_frames
        if vidas <= 0: return
        contador_frames += 1
        delay = max(14, FRAME_ENE)
        if contador_frames < delay: return
        contador_frames = 0
        nuevos, ocup = [], set()
        for ex, ey in enemigos:
            paso = None
            if distancia_manhattan((ex,ey), (pos_x,pos_y)) <= RANGO and powerup_activo != 'invisible':
                p = bfs_siguiente_paso(LABERINTO, (ex,ey), (pos_x,pos_y))
                if p and p not in ocup: paso = p
            if not paso:
                for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nx, ny = ex + dx, ey + dy
                    if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0 and (nx,ny) not in ocup:
                        paso = (nx,ny); break
            ex, ey = paso or (ex,ey)
            if (ex,ey) == (pos_x,pos_y) and powerup_activo != 'invulnerable':
                self.mgr.publicar(EventoColisionEnemigo((pos_x,pos_y),(ex,ey)))
            ocup.add((ex,ey)); nuevos.append((ex,ey))
        enemigos = nuevos

class ManejadorColisiones:
    def __init__(self, mgr): mgr.registrar(EventoColisionEnemigo, self); self.mgr = mgr
    def notificar(self, e):
        global vidas, pos_x, pos_y, puntuacion_final, estado
        vidas -= 1
        if vidas > 0:
            pos_x, pos_y = jugador_celda_libre()
        else:
            puntuacion_final = puntuacion
            estado = "GAME_OVER"

class ManejadorEstrellas:
    def __init__(self, mgr): mgr.registrar(EventoRecogerEstrella, self)
    def notificar(self, e):
        global estrellas, puntuacion
        if isinstance(e, EventoRecogerEstrella) and e.posicion in estrellas:
            estrellas.remove(e.posicion)
            puntuacion += 10
            if not estrellas:
                avanzar_nivel()
                vista.titulo = f"Maze-Run - Nivel {nivel_actual+1}"

class ManejadorMenu:
    def __init__(self, mgr): mgr.registrar(EventoSeleccionMenu, self)
    def notificar(self, e):
        global estado
        if e.opcion == "JUEGO":
            reiniciar_juego(); estado = "JUEGO"
        elif e.opcion == "SALIR":
            pygame.quit(); exit()
        else:
            estado = e.opcion

ControladorJugador(evento_mgr)
ManejadorPowerUps(evento_mgr)
controlador_enemigos = ControladorEnemigos(evento_mgr)
ManejadorColisiones(evento_mgr)
ManejadorEstrellas(evento_mgr)
ManejadorMenu(evento_mgr)

# Bucle principal
while True:
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit(); exit()

        if estado == "MENU":
            menu.manejar_eventos(ev)

        elif estado == "JUEGO":
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    estado = "MENU"
                elif ev.key == pygame.K_UP:    held_dirs.add('arriba');  player_step_timer = 0
                elif ev.key == pygame.K_DOWN:  held_dirs.add('abajo');   player_step_timer = 0
                elif ev.key == pygame.K_LEFT:  held_dirs.add('izquierda'); player_step_timer = 0
                elif ev.key == pygame.K_RIGHT: held_dirs.add('derecha'); player_step_timer = 0
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_UP:    held_dirs.discard('arriba')
                elif ev.key == pygame.K_DOWN:  held_dirs.discard('abajo')
                elif ev.key == pygame.K_LEFT:  held_dirs.discard('izquierda')
                elif ev.key == pygame.K_RIGHT: held_dirs.discard('derecha')

    # Movimiento continuo
    if estado == "JUEGO":
        if held_dirs:
            player_step_timer -= 1
            if player_step_timer <= 0:
                if 'arriba' in held_dirs:   evento_mgr.publicar(EventoMoverJugador('arriba'))
                elif 'abajo' in held_dirs:  evento_mgr.publicar(EventoMoverJugador('abajo'))
                elif 'izquierda' in held_dirs: evento_mgr.publicar(EventoMoverJugador('izquierda'))
                elif 'derecha' in held_dirs:   evento_mgr.publicar(EventoMoverJugador('derecha'))
                player_step_timer = PLAYER_STEP_DELAY

        # lógica y render
        if vidas > 0 and (pos_x,pos_y) in estrellas:
            evento_mgr.publicar(EventoRecogerEstrella((pos_x,pos_y)))
        if vidas > 0 and (pos_x,pos_y) in powerups:
            powerups.remove((pos_x,pos_y)); evento_mgr.publicar(EventoPowerUpAgarrado('congelar'))
        controlador_enemigos.actualizar()

        vista.limpiar_pantalla((0,0,0))
        lvl = NIVELES[nivel_actual]
        col_pared = tuple(lvl.get("colores", {}).get("pared", (80,80,80)))
        col_suelo = tuple(lvl.get("colores", {}).get("suelo", (220,220,220)))
        col_enem = tuple(lvl.get("colores", {}).get("enemigo", (220,50,50)))
        vista.dibujar_laberinto(LABERINTO, TAM_CELDA, col_pared, col_suelo)
        for ex,ey in enemigos: vista.dibujar_enemigo(ex*TAM_CELDA, ey*TAM_CELDA, TAM_CELDA, color=col_enem)
        for sx,sy in estrellas: vista.dibujar_estrella(sx*TAM_CELDA, sy*TAM_CELDA, TAM_CELDA)
        for px,py in powerups: vista.dibujar_powerup(px*TAM_CELDA, py*TAM_CELDA, TAM_CELDA)
        vista.dibujar_jugador(pos_x*TAM_CELDA, pos_y*TAM_CELDA, TAM_CELDA)
        vista.dibujar_hud(vidas, puntuacion)
        vista.actualizar()

    elif estado == "MENU":
        menu.dibujar(); vista.actualizar()

    reloj.tick(FPS)
