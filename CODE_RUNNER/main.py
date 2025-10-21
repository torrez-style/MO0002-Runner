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

# Utilidades de I/O con manejo robusto de errores
def cargar_json(path, default=None):
    """Carga un archivo JSON de manera segura, retornando default si hay error"""
    if not os.path.exists(path):
        return default if default is not None else []
    
    try:
        with open(path, "r", encoding='utf-8') as f:
            content = f.read().strip()
            if not content:  # Archivo vacío
                return default if default is not None else []
            return json.loads(content)
    except (json.JSONDecodeError, IOError, UnicodeDecodeError) as e:
        print(f"Error al cargar {path}: {e}")
        return default if default is not None else []

def guardar_json(path, data):
    """Guarda datos en formato JSON de manera segura"""
    try:
        with open(path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except (IOError, TypeError) as e:
        print(f"Error al guardar {path}: {e}")
        return False

# Carga NIVELES desde JSON con fallback
try:
    datos_niveles = cargar_json(ARCHIVO_NIVELES, {
        "niveles": [
            {
                "laberinto": [
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,0,1,1,0,1,1,1,1,1,1,1,0,0,1],
                    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                ],
                "vel_enemigos": 10,
                "estrellas": 3,
                "enemigos": 2,
                "powerups": 2
            }
        ]
    })
    NIVELES = datos_niveles.get("niveles", [])
    if not NIVELES:
        raise ValueError("No se encontraron niveles válidos")
except Exception as e:
    print(f"Error cargando niveles: {e}. Usando niveles por defecto.")
    NIVELES = [
        {
            "laberinto": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,1,1,0,1,1,1,1,1,1,1,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ],
            "vel_enemigos": 10,
            "estrellas": 3,
            "enemigos": 2,
            "powerups": 2
        },
        {
            "laberinto": [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
                [1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],
                [1,0,0,0,1,0,0,0,1,0,0,0,1,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            ],
            "vel_enemigos": 8,
            "estrellas": 4,
            "enemigos": 3,
            "powerups": 2
        }
    ]

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

def cargar_perfiles():
    return cargar_json(ARCHIVO_PERFILES, [])

def cargar_puntuaciones():
    return cargar_json(ARCHIVO_PUNTUACIONES, [])

def cargar_config():
    return cargar_json(ARCHIVO_CONFIG, {"admin": "123admin"})

def nombre_existe(n):
    perfiles = cargar_perfiles()
    return n.upper() in [p.upper() for p in perfiles if isinstance(p, str)]

def guardar_perfil(n):
    perf = cargar_perfiles()
    if nombre_existe(n):
        return False
    perf.append(n)
    return guardar_json(ARCHIVO_PERFILES, perf)

def guardar_puntuacion(n, p):
    pts = cargar_puntuaciones()
    pts.append({"nombre": n, "puntuacion": p})
    pts = sorted(pts, key=lambda x: x.get("puntuacion", 0), reverse=True)[:10]
    guardar_json(ARCHIVO_PUNTUACIONES, pts)

def guardar_config(cfg):
    return guardar_json(ARCHIVO_CONFIG, cfg)

def borrar_salon():
    return guardar_json(ARCHIVO_PUNTUACIONES, [])

def borrar_perfiles():
    return guardar_json(ARCHIVO_PERFILES, [])

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
            if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0:
                pos_x, pos_y = nx, ny

class ManejadorPowerUps:
    def __init__(self, mgr): mgr.registrar(EventoPowerUpAgarrado, self)
    def notificar(self, e):
        global powerup_activo, powerup_timer
        if isinstance(e, EventoPowerUpAgarrado):
            powerup_activo = e.tipo
            powerup_timer = DURACION_POWERUP

class ControladorEnemigos:
    def __init__(self, mgr): self.mgr = mgr
    def actualizar(self):
        global enemigos, contador_frames
        if vidas <= 0: return
        contador_frames += 1
        delay = FRAME_ENE // 2 if powerup_activo == 'congelar' else FRAME_ENE
        if contador_frames < delay: return
        contador_frames = 0
        nuevos, ocup = [], set()
        for ex, ey in enemigos:
            dist = distancia_manhattan((ex,ey), (pos_x,pos_y))
            paso = None
            if dist <= RANGO and powerup_activo != 'invisible':
                p = bfs_siguiente_paso(LABERINTO, (ex,ey), (pos_x,pos_y))
                if p and p not in ocup: paso = p
            if not paso:
                dirs = [(0,1),(0,-1),(1,0),(-1,0)]
                random.shuffle(dirs)
                for dx, dy in dirs:
                    nx, ny = ex + dx, ey + dy
                    if 0 <= ny < len(LABERINTO) and 0 <= nx < len(LABERINTO[0]) and LABERINTO[ny][nx] == 0 and (nx,ny) not in ocup:
                        paso = (nx,ny)
                        break
            ex, ey = paso or (ex,ey)
            if (ex,ey) == (pos_x,pos_y) and powerup_activo != 'invulnerable':
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
            elif e.opcion == "SALIR":
                pygame.quit()
                exit()
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

        elif estado == "SALÓN_DE_LA_FAMA" and ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            estado = "MENU"

        elif estado == "ADMINISTRACION" and ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                estado = "MENU"
            # Aquí iría el resto del manejo de administración
            # que estaba en el código original pero incompleto

    # Actualizar powerup timer
    if powerup_activo:
        powerup_timer -= 1
        if powerup_timer <= 0: 
            powerup_activo = None

    if estado == "MENU":
        menu.dibujar()
        vista.actualizar()
    
    elif estado == "JUEGO":
        # Lógica del juego
        if vidas > 0 and (pos_x,pos_y) in estrellas:
            evento_mgr.publicar(EventoRecogerEstrella((pos_x,pos_y)))
        
        if vidas > 0 and (pos_x,pos_y) in powerups:
            tipo = random.choice(['invulnerable','congelar','invisible'])
            powerups.remove((pos_x,pos_y))
            evento_mgr.publicar(EventoPowerUpAgarrado(tipo))
        
        controlador_enemigos.actualizar()
        
        # Renderizado
        vista.limpiar_pantalla((0,0,0))
        vista.dibujar_laberinto(LABERINTO, TAM_CELDA)
        
        for ex,ey in enemigos: 
            vista.dibujar_enemigo(ex*TAM_CELDA, ey*TAM_CELDA, TAM_CELDA)
        
        for sx,sy in estrellas: 
            vista.dibujar_estrella(sx*TAM_CELDA, sy*TAM_CELDA, TAM_CELDA)
        
        for px,py in powerups: 
            if hasattr(vista, 'dibujar_powerup'):
                vista.dibujar_powerup(px*TAM_CELDA, py*TAM_CELDA, TAM_CELDA)
        
        vista.dibujar_jugador(pos_x*TAM_CELDA, pos_y*TAM_CELDA, TAM_CELDA)
        vista.dibujar_hud(vidas, puntuacion)
        vista.dibujar_texto(f"Nivel:{nivel_actual+1}", 10, 560, 24, (255,255,255))
        vista.dibujar_texto(f"P-UP:{powerup_activo or 'ninguno'}", 200, 560, 24, (255,255,0))
        vista.actualizar()
    
    elif estado == "GAME_OVER":
        vista.limpiar_pantalla((50,0,0))
        vista.dibujar_texto("GAME OVER", 180, 200, 64, (255,0,0))
        vista.dibujar_texto(f"Punt.Fin:{puntuacion_final}", 150, 280, 36, (255,255,255))
        vista.dibujar_texto("ENTER reint.", 100, 350, 28, (200,200,200))
        vista.dibujar_texto("ESC menu", 90, 390, 28, (200,200,200))
        vista.actualizar()
    
    elif estado == "SALÓN_DE_LA_FAMA":
        vista.limpiar_pantalla((0,0,50))
        vista.dibujar_texto("Salón de la Fama", 150, 250, 48, (255,255,0))
        puntuaciones = cargar_puntuaciones()
        y_pos = 300
        for i, entrada in enumerate(puntuaciones[:10]):
            if isinstance(entrada, dict) and 'nombre' in entrada and 'puntuacion' in entrada:
                texto = f"{i+1}. {entrada['nombre']}: {entrada['puntuacion']}"
                vista.dibujar_texto(texto, 50, y_pos, 24, (255,255,255))
                y_pos += 30
        vista.dibujar_texto("ESC volver", 120, 550, 32, (200,200,200))
        vista.actualizar()
    
    elif estado == "ADMINISTRACION":
        vista.limpiar_pantalla((50,0,0))
        vista.dibujar_texto("Administración", 180, 250, 48, (255,255,0))
        vista.dibujar_texto("ESC volver", 120, 350, 32, (200,200,200))
        if mensaje_error:
            vista.dibujar_texto(mensaje_error, 50, 300, 24, (255,100,100))
        vista.actualizar()

    reloj.tick(60)
