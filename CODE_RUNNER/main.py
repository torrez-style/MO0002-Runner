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

# --- CONFIGURACIÓN ---
ANCHO, ALTO = 600, 600
TAM_CELDA = 40
RANGO = 10
DURACION_POWERUP = 300
ARCHIVO_PUNTUACIONES = "puntuaciones.json"
ARCHIVO_PERFILES = "perfiles.json"
ARCHIVO_CONFIG = "config.json"
ARCHIVO_NIVELES = "niveles.json"

# Carga NIVELES desde JSON
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

# Utilidades de I/O
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

# Posiciones
def generar_posiciones_validas(lab, c, ex):
    pos = []
    filas, cols = len(lab), len(lab[0])
    i = 0
    while len(pos) < c and i < c * 50:
        x, y = random.randint(1, cols-2), random.randint(1, filas-2)
        if lab[y][x] == 0 and (x,y) not in ex + pos:
            pos.append((x,y))
        i += 1
    return pos

def jugador_celda_libre():
    libres = [
        (x,y)
        for y in range(1, len(LABERINTO)-1)
        for x in range(1, len(LABERINTO[0])-1)
        if LABERINTO[y][x] == 0 and (x,y) not in enemigos
    ]
    return random.choice(libres) if libres else (1,1)

def reiniciar_juego():
    global pos_x, pos_y, estrellas, enemigos, powerups, vidas, puntuacion, contador_frames, powerup_activo, powerup_timer
    pos_x, pos_y = 1, 1
    lvl = NIVELES[nivel_actual]
    LAB = lvl["laberinto"]
    estrellas = generar_posiciones_validas(LAB, lvl["estrellas"], [(pos_x,pos_y)])
    enemigos = generar_posiciones_validas(LAB, lvl["enemigos"], [(pos_x,pos_y)] + estrellas)
    powerups = generar_posiciones_validas(LAB, lvl["powerups"], [(pos_x,pos_y)] + estrellas + enemigos)
    vidas, puntuacion, contador_frames = 3, 0, 0
    powerup_activo, powerup_timer = None, 0

def avanzar_nivel():
    global nivel_actual, LABERINTO, FRAME_ENE
    if nivel_actual < len(NIVELES)-1:
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
            if LABERINTO[ny][nx] == 0:
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
        if contador_frames < FRAME_ENE: return
        contador_frames = 0
        nuevos, ocup = [], set()
        for ex, ey in enemigos:
            dist = distancia_manhattan((ex,ey), (pos_x,pos_y))
            paso = None
            if dist <= RANGO:
                p = bfs_siguiente_paso(LABERINTO, (ex,ey), (pos_x,pos_y))
                if p and p not in ocup: paso = p
            if not paso:
                dirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = ex + dx, ey + dy
                    if LABERINTO[ny][nx] == 0 and (nx,ny) not in ocup:
                        paso = (nx,ny)
                        break
            ex, ey = paso or (ex,ey)
            if (ex,ey) == (pos_x,pos_y):
                self.mgr.publicar(EventoColisionEnemigo((pos_x,pos_y),(ex,ey)))
            ocup.add((ex,ey))
            nuevos.append((ex,ey))
        enemigos = nuevos

class ManejadorColisiones:
    def __init__(self, mgr): mgr.registrar(EventoColisionEnemigo, self); self.mgr = mgr
    def notificar(self, e):
        global vidas, pos_x, pos_y, puntuacion_final, estado
        if isinstance(e, EventoColisionEnemigo):
            vidas -= 1
            if vidas > 0:
                pos_x, pos_y = jugador_celda_libre()
            else:
                puntuacion_final = puntuacion
                if perfil_actual:
                    guardar_puntuacion(perfil_actual, puntuacion_final)
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
        if isinstance(e, EventoSeleccionMenu):
            if e.opcion == "JUEGO":
                if not perfil_actual:
                    estado = "ADMINISTRACION"
                else:
                    reiniciar_juego()
                    estado = "JUEGO"
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
    if tiempo_mensaje > 0:
        tiempo_mensaje -= 1
        if tiempo_mensaje <= 0:
            mensaje_error = ""

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

        elif estado == "SALON_FAMA" and ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            estado = "MENU"

        elif estado == "ADMINISTRACION" and ev.type == pygame.KEYDOWN:
            # (mismo manejo de perfiles, contraseñas y borrados según modo_borrar)
            # ...
            pass

    # Dibujado según estado (igual que antes)
    # ...

    reloj.tick(60)
