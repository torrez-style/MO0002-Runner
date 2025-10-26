import pygame
import json
import os
import random
from evento import (
    EventoMoverJugador, EventoSeleccionMenu, EventoColisionEnemigo,
    EventoRecogerEstrella, EventoPowerUpAgarrado, AdministradorDeEventos
)
from vista import Vista
from menu import MenuPrincipal
from pathfinding import bfs_siguiente_paso

class Juego:
    def __init__(self, ancho=900, alto=700, fps=50, niveles_path="niveles.json"):
        self.ANCHO, self.ALTO = ancho, alto
        self.FPS = fps
        self.DURACION_POWERUP = 300
        self.niveles_path = niveles_path
        self.niveles = self._cargar_niveles()
        self.nivel_actual = 0
        
        # Fix para IndexError: Validar que existan niveles cargados
        if not self.niveles or len(self.niveles) == 0:
            # Crear nivel de emergencia si no hay niveles cargados
            self.niveles = [self._crear_nivel_emergencia()]
            self.sin_niveles_cargados = True
        else:
            self.sin_niveles_cargados = False
            
        self.LABERINTO = self.niveles[0]["laberinto"]
        self.FRAME_ENE = max(12, self.niveles[0].get("vel_enemigos", 18))
        self.tam_celda = 32
        self.pos_x = 1; self.pos_y = 1
        self.estrellas = []
        self.enemigos = []
        self.powerups = []
        self.vidas = 3
        self.puntuacion = 0
        self.contador_frames = 0
        self.powerup_timer = 0
        self.powerup_activo = None
        self.puntuacion_final = 0
        self.estado = "MENU"
        self.texto_mensaje = ""
        self.mensaje_frames = 0
        self.PLAYER_STEP_DELAY = 7
        self.player_step_timer = 0
        self.held_dirs = set()
        pygame.init()
        self.reloj = pygame.time.Clock()
        self.vista = Vista(self.ANCHO, self.ALTO, f"Maze-Run - Nivel {self.nivel_actual+1}")
        self.evento_mgr = AdministradorDeEventos()
        self.menu = MenuPrincipal(self.vista, self.evento_mgr)
        self._registrar_manejadores()
        self._configurar_tablero()
        self._reiniciar_juego()

    def _crear_nivel_emergencia(self):
        """Crear un nivel básico cuando no hay niveles cargados"""
        return {
            "nombre": "Nivel de Emergencia - Carga laberintos desde Administración",
            "laberinto": [
                [1,1,1,1,1,1,1,1,1,1],
                [1,2,0,0,0,0,0,0,3,1],
                [1,0,1,1,1,1,1,0,0,1],
                [1,0,0,0,0,0,0,0,1,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            "vel_enemigos": 20,
            "estrellas": 1,
            "enemigos": 0,
            "powerups": 0,
            "entrada": [1, 1],
            "salida": [8, 1],
            "colores": {
                "pared": [100,100,100], 
                "suelo": [200,200,200], 
                "enemigo": [220,50,50], 
                "salida": [0,255,0]
            }
        }

    def _cargar_niveles(self):
        """Cargar niveles desde archivo JSON con manejo de errores mejorado"""
        try:
            # Construir ruta completa
            ruta_completa = os.path.join("CODE_RUNNER", self.niveles_path)
            if not os.path.exists(ruta_completa):
                ruta_completa = self.niveles_path  # Fallback a ruta original
            
            with open(ruta_completa, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            if "niveles" in data and isinstance(data["niveles"], list):
                return data["niveles"]
            else:
                return []  # Retornar lista vacía si no hay estructura correcta
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as ex:
            print(f"Error cargando niveles: {ex}")
            return []  # Retornar lista vacía en caso de error

    def _reload_niveles(self):
        """Recargar niveles desde archivo - usado después de carga administrativa"""
        nuevos_niveles = self._cargar_niveles()
        
        if nuevos_niveles and len(nuevos_niveles) > 0:
            self.niveles = nuevos_niveles
            self.sin_niveles_cargados = False
            self.nivel_actual = 0
            self.LABERINTO = self.niveles[0]["laberinto"]
            self._configurar_tablero()
            self._reiniciar_juego()
            self.vista.titulo = "Maze-Run - Nivel 1 (nuevos niveles cargados)"
            
            # Mostrar mensaje de confirmación
            self.texto_mensaje = f"¡{len(nuevos_niveles)} laberinto(s) cargado(s) exitosamente!"
            self.mensaje_frames = 180  # 3.6 segundos a 50 FPS
        else:
            # Mantener nivel de emergencia si no se cargaron niveles válidos
            self.texto_mensaje = "No se encontraron laberintos válidos"
            self.mensaje_frames = 120

    def _configurar_tablero(self):
        filas, cols = len(self.LABERINTO), len(self.LABERINTO[0])
        area_w, area_h = 800, 600
        tablero_w = self.tam_celda * cols
        tablero_h = self.tam_celda * filas
        self.vista.offset_x = (self.vista.ancho - tablero_w) // 2
        self.vista.offset_y = (self.vista.alto - tablero_h) // 2 + 20

    def _generar_posiciones_validas(self, lab, c, ex):
        pos = []
        filas, cols = len(lab), len(lab[0])
        i = 0
        while len(pos) < c and i < c * 50:
            x, y = random.randint(1, cols - 2), random.randint(1, filas - 2)
            if lab[y][x] == 0 and (x, y) not in ex + pos:
                pos.append((x, y))
            i += 1
        return pos

    def _jugador_celda_libre(self):
        libres = [
            (x, y)
            for y in range(1, len(self.LABERINTO) - 1)
            for x in range(1, len(self.LABERINTO[0]) - 1)
            if self.LABERINTO[y][x] == 0 and (x, y) not in self.enemigos
        ]
        return random.choice(libres) if libres else (1, 1)

    def _reiniciar_juego(self):
        # Verificar que el índice de nivel sea válido
        if self.nivel_actual >= len(self.niveles):
            self.nivel_actual = 0
        
        lvl = self.niveles[self.nivel_actual]
        self.LABERINTO = lvl["laberinto"]
        self.pos_x, self.pos_y = self._jugador_celda_libre()
        exclusiones = [self.pos_x, self.pos_y]
        self.estrellas = self._generar_posiciones_validas(self.LABERINTO, lvl.get("estrellas", 3), exclusiones)
        self.enemigos = self._generar_posiciones_validas(self.LABERINTO, lvl.get("enemigos", 2), exclusiones + self.estrellas)
        self.powerups = self._generar_posiciones_validas(self.LABERINTO, lvl.get("powerups", 2), exclusiones + self.estrellas + self.enemigos)
        self.vidas = 3
        self.contador_frames = 0
        self.powerup_activo, self.powerup_timer = None, 0
        self.texto_mensaje = ""
        self.mensaje_frames = 0

    def _avanzar_nivel(self):
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1
            lvl = self.niveles[self.nivel_actual]
            self.LABERINTO = lvl["laberinto"]
            self.FRAME_ENE = max(10, lvl.get("vel_enemigos", 12))
            self._configurar_tablero()
            self._reiniciar_juego()
            self.vista.titulo = f"Maze-Run - Nivel {self.nivel_actual+1}"
        else:
            self._estado_cambiar_a_game_over()

    def _estado_cambiar_a_game_over(self):
        self.puntuacion_final = self.puntuacion
        self.estado = "GAME_OVER"

    def _registrar_manejadores(self):
        class ControladorJugador:
            def __init__(self, juego, mgr): self.juego=juego; mgr.registrar(EventoMoverJugador, self)
            def notificar(self, e):
                j=self.juego
                if j.vidas<=0: return
                dx=dy=0
                if e.direccion=='arriba': dy=-1
                elif e.direccion=='abajo': dy=1
                elif e.direccion=='izquierda': dx=-1
                elif e.direccion=='derecha': dx=1
                nx,ny=j.pos_x+dx,j.pos_y+dy
                if 0<=ny<len(j.LABERINTO) and 0<=nx<len(j.LABERINTO[0]) and j.LABERINTO[ny][nx] == 0:
                    j.pos_x,j.pos_y=nx,ny
        
        class ManejadorPowerUps:
            def __init__(self, juego, mgr): self.juego=juego; mgr.registrar(EventoPowerUpAgarrado, self)
            def notificar(self, e):
                j=self.juego; j.powerup_activo=e.tipo; j.powerup_timer=j.DURACION_POWERUP
        
        class ControladorEnemigos:
            def __init__(self, juego, mgr): self.j=juego
            def actualizar(self):
                j=self.j
                if j.vidas<=0: return
                j.contador_frames+=1
                delay=max(14,j.FRAME_ENE)
                if j.contador_frames<delay: return
                j.contador_frames=0
                nuevos,ocup=[],set()
                for ex,ey in j.enemigos:
                    paso=None
                    if j.powerup_activo!='invisible':
                        p=bfs_siguiente_paso(j.LABERINTO,(ex,ey),(j.pos_x,j.pos_y))
                        if p and p not in ocup: paso=p
                    if not paso:
                        for dx,dy in [(0,1),(0,-1),(1,0),(-1,0)]:
                            nx,ny=ex+dx,ey+dy
                            if 0<=ny<len(j.LABERINTO) and 0<=nx<len(j.LABERINTO[0]) and j.LABERINTO[ny][nx] == 0 and (nx,ny) not in ocup:
                                paso=(nx,ny); break
                    ex,ey=paso or (ex,ey)
                    if (ex,ey)==(j.pos_x,j.pos_y) and j.powerup_activo!='invulnerable':
                        j.evento_mgr.publicar(EventoColisionEnemigo((j.pos_x,j.pos_y),(ex,ey)))
                    ocup.add((ex,ey)); nuevos.append((ex,ey))
                j.enemigos=nuevos
        
        class ManejadorColisiones:
            def __init__(self, juego, mgr): self.j=juego; mgr.registrar(EventoColisionEnemigo, self)
            def notificar(self, e):
                j=self.j; j.vidas-=1
                if j.vidas>0:
                    j.pos_x,j.pos_y=j._jugador_celda_libre()
                else:
                    j._estado_cambiar_a_game_over()
        
        class ManejadorEstrellas:
            def __init__(self, juego, mgr): self.j=juego; mgr.registrar(EventoRecogerEstrella, self)
            def notificar(self, e):
                j=self.j
                if e.posicion in j.estrellas:
                    j.estrellas.remove(e.posicion)
                    j.puntuacion+=10
                    if not j.estrellas:
                        j._avanzar_nivel()
        
        class ManejadorMenu:
            def __init__(self, juego, mgr): self.j=juego; mgr.registrar(EventoSeleccionMenu, self)
            def notificar(self, e):
                j=self.j
                if e.opcion=="JUEGO": 
                    # Solo iniciar si no estamos en modo emergencia o hay niveles reales
                    if not j.sin_niveles_cargados:
                        j.nivel_actual=0; j._reiniciar_juego(); j.estado="JUEGO"
                    else:
                        j.texto_mensaje = "Debe cargar laberintos desde Administración primero"
                        j.mensaje_frames = 120
                elif e.opcion=="SALIR": pygame.quit(); exit()
                elif e.opcion=="ADMINISTRACION": j._reload_niveles(); j.estado="MENU"
                else: j.estado=e.opcion
        
        self.controlador_enemigos = ControladorEnemigos(self, self.evento_mgr)
        ControladorJugador(self, self.evento_mgr)
        ManejadorPowerUps(self, self.evento_mgr)
        ManejadorColisiones(self, self.evento_mgr)
        ManejadorEstrellas(self, self.evento_mgr)
        ManejadorMenu(self, self.evento_mgr)

    def run(self):
        while True:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT:
                    pygame.quit(); exit()
                if self.estado=="MENU":
                    self.menu.manejar_eventos(ev)
                elif self.estado=="JUEGO":
                    if ev.type==pygame.KEYDOWN:
                        if ev.key==pygame.K_ESCAPE: self.estado="MENU"
                        elif ev.key==pygame.K_UP: self.held_dirs.add('arriba'); self.player_step_timer=0
                        elif ev.key==pygame.K_DOWN: self.held_dirs.add('abajo'); self.player_step_timer=0
                        elif ev.key==pygame.K_LEFT: self.held_dirs.add('izquierda'); self.player_step_timer=0
                        elif ev.key==pygame.K_RIGHT: self.held_dirs.add('derecha'); self.player_step_timer=0
                    elif ev.type==pygame.KEYUP:
                        if ev.key==pygame.K_UP: self.held_dirs.discard('arriba')
                        elif ev.key==pygame.K_DOWN: self.held_dirs.discard('abajo')
                        elif ev.key==pygame.K_LEFT: self.held_dirs.discard('izquierda')
                        elif ev.key==pygame.K_RIGHT: self.held_dirs.discard('derecha')
                elif self.estado=="GAME_OVER":
                    if ev.type==pygame.KEYDOWN:
                        if ev.key==pygame.K_ESCAPE: self.estado="MENU"
                        elif ev.key==pygame.K_RETURN: 
                            if not self.sin_niveles_cargados:
                                self.nivel_actual=0; self._reiniciar_juego(); self.estado="JUEGO"
                elif self.estado=="SALÓN_DE_LA_FAMA":
                    if ev.type==pygame.KEYDOWN and ev.key==pygame.K_ESCAPE:
                        self.estado="MENU"

            if self.estado=="JUEGO":
                if self.held_dirs:
                    self.player_step_timer-=1
                    if self.player_step_timer<=0:
                        if 'arriba' in self.held_dirs: self.evento_mgr.publicar(EventoMoverJugador('arriba'))
                        elif 'abajo' in self.held_dirs: self.evento_mgr.publicar(EventoMoverJugador('abajo'))
                        elif 'izquierda' in self.held_dirs: self.evento_mgr.publicar(EventoMoverJugador('izquierda'))
                        elif 'derecha' in self.held_dirs: self.evento_mgr.publicar(EventoMoverJugador('derecha'))
                        self.player_step_timer=self.PLAYER_STEP_DELAY
                # Recoger estrellas y auto-avanzar nivel
                if self.vidas>0 and (self.pos_x,self.pos_y) in self.estrellas:
                    self.evento_mgr.publicar(EventoRecogerEstrella((self.pos_x,self.pos_y)))
                # Recoger powerups
                if self.vidas>0 and (self.pos_x,self.pos_y) in self.powerups:
                    self.powerups.remove((self.pos_x,self.pos_y)); self.evento_mgr.publicar(EventoPowerUpAgarrado(random.choice(['invulnerable','congelar','invisible'])))
                if self.mensaje_frames>0:
                    self.mensaje_frames-=1
                self.controlador_enemigos.actualizar()

                # Render
                self.vista.limpiar_pantalla((0,0,0))
                lvl=self.niveles[self.nivel_actual]
                col_pared=tuple(lvl.get("colores",{}).get("pared",(80,80,80)))
                col_suelo=tuple(lvl.get("colores",{}).get("suelo",(220,220,220)))
                col_enem=tuple(lvl.get("colores",{}).get("enemigo",(220,50,50)))
                self.vista.dibujar_laberinto(self.LABERINTO,self.tam_celda,col_pared,col_suelo)
                for ex,ey in self.enemigos: self.vista.dibujar_enemigo(ex*self.tam_celda,ey*self.tam_celda,self.tam_celda,color=col_enem)
                for sx,sy in self.estrellas: self.vista.dibujar_estrella(sx*self.tam_celda,sy*self.tam_celda,self.tam_celda)
                for px,py in self.powerups: self.vista.dibujar_powerup(px*self.tam_celda,py*self.tam_celda,self.tam_celda)
                self.vista.dibujar_jugador(self.pos_x*self.tam_celda,self.pos_y*self.tam_celda,self.tam_celda)
                self.vista.dibujar_hud(self.vidas,self.puntuacion)
                
                # Mostrar mensaje si estamos en modo emergencia
                if self.sin_niveles_cargados:
                    self.vista.dibujar_texto("MODO DEMO - Cargar laberintos desde Administración", 50, 30, 24, (255,200,100))
                
                if self.texto_mensaje and self.mensaje_frames>0:
                    self.vista.dibujar_texto(self.texto_mensaje, 120, 60, 32, (255,64,64))
                self.vista.actualizar()

            elif self.estado=="MENU":
                self.menu.dibujar(); self.vista.actualizar()
            elif self.estado=="GAME_OVER":
                self.vista.limpiar_pantalla((30,0,0))
                self.vista.dibujar_texto("GAME OVER", 220, 200, 72, (255,80,80))
                self.vista.dibujar_texto(f"Puntaje final: {self.puntuacion_final}", 200, 280, 36, (255,255,255))
                if not self.sin_niveles_cargados:
                    self.vista.dibujar_texto("ENTER: Reintentar    ESC: Menú", 160, 340, 28, (220,220,220))
                else:
                    self.vista.dibujar_texto("ESC: Menú (Cargar laberintos desde Admin)", 120, 340, 28, (220,220,220))
                self.vista.actualizar()
            elif self.estado=="SALÓN_DE_LA_FAMA":
                self.vista.limpiar_pantalla((0,0,50))
                self.vista.dibujar_texto("Salón de la Fama", 150, 200, 48, (255,255,0))
                puntuaciones = self._cargar_json("puntuaciones.json", [])
                y_pos = 270
                for i, entrada in enumerate(puntuaciones[:10]):
                    if isinstance(entrada, dict) and 'nombre' in entrada and 'puntuacion' in entrada:
                        self.vista.dibujar_texto(f"{i+1}. {entrada['nombre']}: {entrada['puntuacion']}", 120, y_pos, 24, (255,255,255))
                        y_pos += 30
                self.vista.dibujar_texto("ESC: Volver", 120, 550, 32, (200,200,200))
                self.vista.actualizar()
            elif self.estado=="ADMINISTRACION":
                self.vista.limpiar_pantalla((50,0,0))
                self.vista.dibujar_texto("Administración", 180, 250, 48, (255,255,0))
                self.vista.dibujar_texto("ESC: Volver", 120, 350, 32, (200,200,200))
                self._reload_niveles()
                self.estado = "MENU"
                self.vista.actualizar()

            self.reloj.tick(self.FPS)

    def _cargar_json(self, path, default=None):
        if not os.path.exists(path):
            return default if default is not None else []
        try:
            with open(path, "r", encoding="utf-8") as f:
                txt = f.read().strip()
                return json.loads(txt) if txt else (default if default is not None else [])
        except json.JSONDecodeError:
            return default if default is not None else []