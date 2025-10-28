import sys
import pygame
import json
import os
import random
from evento import (
    EventoMoverJugador, EventoSeleccionMenu, EventoColisionEnemigo,
    EventoRecogerEstrella, EventoPotenciadorRecogido, AdministradorEventos
)
from vista import Vista
from menu import MenuPrincipal
from pathfinding import encontrar_siguiente_paso_bfs as bfs_siguiente_paso
from constantes import (
    COLOR_FONDO, COLOR_TEXTO, COLOR_TEXTO_DESTACADO,
    COLOR_PARED_DEFAULT, COLOR_SUELO_DEFAULT,
    PUNTOS_POR_ESTRELLA, VIDAS_INICIALES, TAMAÑO_CELDA,
    POTENCIADOR_INVULNERABLE, POTENCIADOR_CONGELAR, POTENCIADOR_INVISIBLE,
    ESTADO_MENU, ESTADO_JUEGO, ESTADO_GAME_OVER, ESTADO_SALON, ESTADO_ADMIN,
    CELDA_PARED, CELDA_VACIA, CELDA_ENTRADA, CELDA_SALIDA,
)
from salon_de_la_fama import SalonDeLaFama
from gestor_perfiles import GestorPerfiles


class Juego:
    def __init__(self, ancho=900, alto=700, fps=50, ruta_niveles="niveles.json"):
        self.ancho, self.alto = ancho, alto
        self.fps = fps
        self.duracion_potenciador = 300
        self.ruta_niveles = ruta_niveles

        self.niveles = self._cargar_niveles()
        self.nivel_actual = 0
        if not self.niveles:
            self.niveles = [self._crear_nivel_emergencia()]
            self.sin_niveles_cargados = True
        else:
            self.sin_niveles_cargados = False

        self.laberinto = self.niveles[0]["laberinto"]
        self.velocidad_enemigos = max(10, self.niveles[0].get("vel_enemigos", 14))
        self.tamano_celda = TAMAÑO_CELDA

        self.posicion_x = 1
        self.posicion_y = 1
        self.estrellas = []
        self.enemigos = []
        self.potenciadores = []
        self.vidas = VIDAS_INICIALES
        self.puntuacion = 0
        self.contador_cuadros = 0
        self.temporizador_potenciador = 0
        self.potenciador_activo = None
        self.puntuacion_final = 0
        self.estado = ESTADO_MENU
        self.mensaje_texto = ""
        self.cuadros_mensaje = 0
        self.retraso_paso_jugador = 7
        self.temporizador_paso_jugador = 0
        self.direcciones_presionadas = set()

        self.salon = SalonDeLaFama()
        self.gestor_perfiles = GestorPerfiles()

        pygame.init()
        self.reloj = pygame.time.Clock()
        self.vista = Vista(self.ancho, self.alto, f"Maze-Run - Nivel {self.nivel_actual + 1}")
        self.administrador_eventos = AdministradorEventos()
        self.menu = MenuPrincipal(self.vista, self.administrador_eventos)
        self._registrar_manejadores()
        self._configurar_tablero()
        self._reiniciar_juego()

    def _crear_nivel_emergencia(self):
        return {
            "nombre": "Emergencia",
            "laberinto": [
                [1,1,1,1,1,1,1,1,1,1],
                [1,2,0,0,0,0,0,0,3,1],
                [1,0,1,1,1,1,1,0,0,1],
                [1,0,0,0,0,0,0,0,1,1],
                [1,1,1,1,1,1,1,1,1,1]
            ],
            "vel_enemigos": 14,
            "estrellas": 3,
            "enemigos": 1,
            "powerups": 0,
            "entrada": [1, 1],
            "salida": [8, 1],
            "colores": {"pared": [100, 100, 100], "suelo": [200, 200, 200], "enemigo": [220, 50, 50]},
        }

    def _cargar_niveles(self):
        try:
            ruta_completa = os.path.join("CODE_RUNNER", self.ruta_niveles)
            if not os.path.exists(ruta_completa):
                ruta_completa = self.ruta_niveles
            with open(ruta_completa, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if "niveles" in datos and isinstance(datos["niveles"], list):
                return datos["niveles"]
            return []
        except Exception as excepcion:
            print(f"Error cargando niveles: {excepcion}")
            return []

    def _hay_camino_entrada_salida(self, lab):
        entrada = salida = None
        for y, fila in enumerate(lab):
            for x, c in enumerate(fila):
                if c == CELDA_ENTRADA: entrada = (x, y)
                elif c == CELDA_SALIDA: salida = (x, y)
        if not entrada or not salida: return False
        grid_bin = [[0 if c != CELDA_PARED else 1 for c in fila] for fila in lab]
        return bfs_siguiente_paso(grid_bin, entrada, salida) is not None

    def _recargar_niveles(self):
        nuevos_niveles = self._cargar_niveles()
        if nuevos_niveles:
            self.niveles = nuevos_niveles
            self.sin_niveles_cargados = False
            self.nivel_actual = 0
            self.laberinto = self.niveles[0]["laberinto"]
            if not self._hay_camino_entrada_salida(self.laberinto):
                print("Nivel 1 inválido: sin camino entrada→salida. Cargando nivel de emergencia.")
                self.niveles = [self._crear_nivel_emergencia()]
                self.laberinto = self.niveles[0]["laberinto"]
            self._configurar_tablero(); self._reiniciar_juego()
            self.vista.titulo = "Maze-Run - Nivel 1 (nuevos niveles cargados)"
            self.mensaje_texto = f"¡{len(self.niveles)} laberinto(s) listo(s)!"; self.cuadros_mensaje = 180
        else:
            self.mensaje_texto = "No se encontraron laberintos válidos"; self.cuadros_mensaje = 120

    def _configurar_tablero(self):
        filas, columnas = len(self.laberinto), len(self.laberinto[0])
        ancho_tablero = self.tamano_celda * columnas; alto_tablero = self.tamano_celda * filas
        self.vista.desplazamiento_x = (self.vista.ancho - ancho_tablero) // 2; self.vista.desplazamiento_y = (self.vista.alto - alto_tablero) // 2 + 20

    def _es_celda_transitable(self, x, y):
        if not (0 <= y < len(self.laberinto) and 0 <= x < len(self.laberinto[0])): return False
        return self.laberinto[y][x] in (CELDA_VACIA, CELDA_ENTRADA, CELDA_SALIDA)

    def _generar_posiciones_validas(self, laberinto, cantidad, exclusiones):
        posiciones = []; filas, columnas = len(laberinto), len(laberinto[0]); intentos = 0
        exclusiones_set = set(exclusiones)
        while len(posiciones) < cantidad and intentos < cantidad * 80:
            x, y = random.randint(1, columnas - 2), random.randint(1, filas - 2)
            if self._es_celda_transitable(x, y) and (x, y) not in exclusiones_set and (x, y) not in posiciones:
                posiciones.append((x, y))
            intentos += 1
        return posiciones

    def _obtener_celda_libre_jugador(self):
        libres = [
            (x, y)
            for y in range(1, len(self.laberinto) - 1)
            for x in range(1, len(self.laberinto[0]) - 1)
            if self._es_celda_transitable(x, y) and (x, y) not in self.enemigos
        ]
        return random.choice(libres) if libres else (1, 1)

    def _recolocar_enemigos_si_vacio(self, nivel):
        if not self.enemigos:
            exclusiones = [(self.posicion_x, self.posicion_y)] + self.estrellas
            self.enemigos = self._generar_posiciones_validas(self.laberinto, max(1, nivel.get("enemigos", 1)), exclusiones)

    def _bonificar_estrellas_restantes(self, nivel_actual):
        # Bonifica estrellas recogidas en el nivel actual
        objetivo_estrellas = nivel_actual.get("estrellas", 0)
        recogidas = max(0, objetivo_estrellas - len(self.estrellas))
        if recogidas > 0: self.puntuacion += PUNTOS_POR_ESTRELLA * recogidas

    def _reiniciar_juego(self):
        if self.nivel_actual >= len(self.niveles): self.nivel_actual = 0
        nivel_actual = self.niveles[self.nivel_actual]
        self.laberinto = nivel_actual["laberinto"]
        if not self._hay_camino_entrada_salida(self.laberinto):
            print("Nivel inválido: sin camino. Usando emergencia."); self.laberinto = self._crear_nivel_emergencia()["laberinto"]
        self.posicion_x, self.posicion_y = self._obtener_celda_libre_jugador()
        exclusiones = [(self.posicion_x, self.posicion_y)]
        objetivo_estrellas = nivel_actual.get("estrellas", 3)
        self.estrellas = self._generar_posiciones_validas(self.laberinto, objetivo_estrellas, exclusiones)
        self.enemigos = self._generar_posiciones_validas(self.laberinto, max(1, nivel_actual.get("enemigos", 1)), exclusiones + self.estrellas)
        self.potenciadores = self._generar_posiciones_validas(self.laberinto, nivel_actual.get("powerups", 1), exclusiones + self.estrellas + self.enemigos)
        self._recolocar_enemigos_si_vacio(nivel_actual)
        self.desplazamiento_interfaz_x = 20; self.desplazamiento_interfaz_y = 48
        self.vidas = VIDAS_INICIALES; self.contador_cuadros = 0; self.potenciador_activo = None; self.temporizador_potenciador = 0; self.congelar_tics = 0
        self.mensaje_texto = ""; self.cuadros_mensaje = 0

    def _ha_llegado_a_salida(self):
        return self.laberinto[self.posicion_y][self.posicion_x] == CELDA_SALIDA

    def _avanzar_nivel(self):
        if not self._ha_llegado_a_salida():
            self.mensaje_texto = "Ve a la salida para continuar"; self.cuadros_mensaje = 60; return
        # Bonificar estrellas recogidas en este nivel antes de pasar
        self._bonificar_estrellas_restantes(self.niveles[self.nivel_actual])
        if self.nivel_actual < len(self.niveles) - 1:
            self.nivel_actual += 1; nivel_actual = self.niveles[self.nivel_actual]
            self.laberinto = nivel_actual["laberinto"]; self.velocidad_enemigos = max(8, nivel_actual.get("vel_enemigos", 12))
            self._configurar_tablero(); self._reiniciar_juego(); self.vista.titulo = f"Maze-Run - Nivel {self.nivel_actual + 1}"
        else:
            self._cambiar_a_victoria()

    def _cambiar_a_victoria(self):
        # Ya se bonificó al pasar el último nivel, registrar y mostrar victoria
        self.puntuacion_final = self.puntuacion
        self._registrar_puntuacion_en_perfiles()
        self.estado = ESTADO_GAME_OVER; self.mensaje_texto = "¡Has ganado!"; self.cuadros_mensaje = 180; self._mostrar_victoria = True

    def _cambiar_a_fin_de_juego(self):
        self.puntuacion_final = self.puntuacion
        self._registrar_puntuacion_en_perfiles()
        self.estado = ESTADO_GAME_OVER; self.mensaje_texto = "GAME OVER"; self.cuadros_mensaje = 180; self._mostrar_victoria = False

    def _registrar_puntuacion_en_perfiles(self):
        if self.gestor_perfiles.registrar_partida(self.puntuacion_final): pass

    def _registrar_manejadores(self):
        class ControladorJugador:
            def __init__(self, juego, administrador): self.juego = juego; administrador.registrar(EventoMoverJugador, self)
            def notificar(self, evento):
                j = self.juego
                if j.vidas <= 0: return
                dx = dy = 0
                if evento.direccion == 'arriba': dy = -1
                elif evento.direccion == 'abajo': dy = 1
                elif evento.direccion == 'izquierda': dx = -1
                elif evento.direccion == 'derecha': dx = 1
                nx, ny = j.posicion_x + dx, j.posicion_y + dy
                if j._es_celda_transitable(nx, ny): j.posicion_x, j.posicion_y = nx, ny
                if (j.posicion_x, j.posicion_y) in j.enemigos and j.potenciador_activo != POTENCIADOR_INVULNERABLE:
                    j.administrador_eventos.publicar(EventoColisionEnemigo((j.posicion_x, j.posicion_y), (j.posicion_x, j.posicion_y)))
                if j._ha_llegado_a_salida(): j._avanzar_nivel()

        class ManejadorPotenciadores:
            def __init__(self, juego, administrador): self.juego = juego; administrador.registrar(EventoPotenciadorRecogido, self)
            def notificar(self, evento):
                j = self.juego; j.potenciador_activo = evento.tipo; j.temporizador_potenciador = j.duracion_potenciador
                if evento.tipo == POTENCIADOR_CONGELAR: j.congelar_tics = j.duracion_potenciador
                j.mensaje_texto = f"Potenciador: {evento.tipo}"; j.cuadros_mensaje = 60

        class ControladorEnemigos:
            def __init__(self, juego, administrador): self.juego = juego
            def actualizar(self):
                j = self.juego
                if j.vidas <= 0: return
                if getattr(j, 'congelar_tics', 0) > 0: j.congelar_tics -= 1; return
                j.contador_cuadros += 1; retraso = max(10, j.velocidad_enemigos)
                if j.contador_cuadros < retraso: return
                j.contador_cuadros = 0
                nuevos, ocupadas = [], set()
                for ex, ey in j.enemigos:
                    objetivo = (j.posicion_x, j.posicion_y)
                    grid_bin = [[0 if c != CELDA_PARED else 1 for c in fila] for fila in j.laberinto]
                    siguiente = bfs_siguiente_paso(grid_bin, (ex, ey), objetivo) if j.potenciador_activo != POTENCIADOR_INVISIBLE else None
                    if not siguiente:
                        dx = 1 if j.posicion_x > ex else -1 if j.posicion_x < ex else 0
                        dy = 1 if j.posicion_y > ey else -1 if j.posicion_y < ey else 0
                        candidatos = [(ex + dx, ey), (ex, ey + dy), (ex + dx, ey + dy), (ex - dx, ey), (ex, ey - dy)]
                        for nx, ny in candidatos:
                            if j._es_celda_transitable(nx, ny) and (nx, ny) not in ocupadas: siguiente = (nx, ny); break
                    ex, ey = siguiente or (ex, ey)
                    if (ex, ey) == (j.posicion_x, j.posicion_y) and j.potenciador_activo != POTENCIADOR_INVULNERABLE:
                        j.administrador_eventos.publicar(EventoColisionEnemigo((j.posicion_x, j.posicion_y), (ex, ey)))
                    ocupadas.add((ex, ey)); nuevos.append((ex, ey))
                j.enemigos = nuevos

        class ManejadorColisiones:
            def __init__(self, juego, administrador): self.juego = juego; administrador.registrar(EventoColisionEnemigo, self)
            def notificar(self, evento):
                j = self.juego; j.vidas -= 1
                if j.vidas > 0: j.posicion_x, j.posicion_y = j._obtener_celda_libre_jugador(); j._recolocar_enemigos_si_vacio(j.niveles[j.nivel_actual])
                else: j._cambiar_a_fin_de_juego()

        class ManejadorEstrellas:
            def __init__(self, juego, administrador): self.juego = juego; administrador.registrar(EventoRecogerEstrella, self)
            def notificar(self, evento):
                j = self.juego
                if evento.posicion in j.estrellas:
                    j.estrellas.remove(evento.posicion); j.puntuacion += PUNTOS_POR_ESTRELLA

        class ManejadorMenu:
            def __init__(self, juego, administrador): self.juego = juego; administrador.registrar(EventoSeleccionMenu, self)
            def notificar(self, evento):
                j = self.juego
                if evento.opcion == ESTADO_JUEGO:
                    if not j.sin_niveles_cargados: j.nivel_actual = 0; j._reiniciar_juego(); j.estado = ESTADO_JUEGO
                    else: j.mensaje_texto = "Debe cargar laberintos desde Administración primero"; j.cuadros_mensaje = 120
                elif evento.opcion == "SALIR": pygame.quit(); sys.exit(0)
                elif evento.opcion == ESTADO_ADMIN: j._recargar_niveles(); j.estado = ESTADO_MENU
                else: j.estado = evento.opcion

        self.controlador_enemigos = ControladorEnemigos(self, self.administrador_eventos)
        ControladorJugador(self, self.administrador_eventos); ManejadorPotenciadores(self, self.administrador_eventos)
        ManejadorColisiones(self, self.administrador_eventos); ManejadorEstrellas(self, self.administrador_eventos); ManejadorMenu(self, self.administrador_eventos)

    def ejecutar(self):
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT: pygame.quit(); sys.exit(0)
                if self.estado == ESTADO_MENU: self.menu.manejar_eventos(evento)
                elif self.estado == ESTADO_JUEGO:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE: self.estado = ESTADO_MENU
                        elif evento.key == pygame.K_UP: self.direcciones_presionadas.add('arriba'); self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_DOWN: self.direcciones_presionadas.add('abajo'); self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_LEFT: self.direcciones_presionadas.add('izquierda'); self.temporizador_paso_jugador = 0
                        elif evento.key == pygame.K_RIGHT: self.direcciones_presionadas.add('derecha'); self.temporizador_paso_jugador = 0
                    elif evento.type == pygame.KEYUP:
                        if evento.key == pygame.K_UP: self.direcciones_presionadas.discard('arriba')
                        elif evento.key == pygame.K_DOWN: self.direcciones_presionadas.discard('abajo')
                        elif evento.key == pygame.K_LEFT: self.direcciones_presionadas.discard('izquierda')
                        elif evento.key == pygame.K_RIGHT: self.direcciones_presionadas.discard('derecha')
                elif self.estado == ESTADO_GAME_OVER:
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE: self.estado = ESTADO_MENU
                        elif evento.key == pygame.K_RETURN and not self.sin_niveles_cargados:
                            self.nivel_actual = 0; self._reiniciar_juego(); self.estado = ESTADO_JUEGO
                elif self.estado == ESTADO_SALON:
                    if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE: self.estado = ESTADO_MENU

            if self.estado == ESTADO_JUEGO:
                if self.direcciones_presionadas:
                    self.temporizador_paso_jugador -= 1
                    if self.temporizador_paso_jugador <= 0:
                        if 'arriba' in self.direcciones_presionadas: self.administrador_eventos.publicar(EventoMoverJugador('arriba'))
                        elif 'abajo' in self.direcciones_presionadas: self.administrador_eventos.publicar(EventoMoverJugador('abajo'))
                        elif 'izquierda' in self.direcciones_presionadas: self.administrador_eventos.publicar(EventoMoverJugador('izquierda'))
                        elif 'derecha' in self.direcciones_presionadas: self.administrador_eventos.publicar(EventoMoverJugador('derecha'))
                        self.temporizador_paso_jugador = self.retraso_paso_jugador

                if self.vidas > 0 and (self.posicion_x, self.posicion_y) in self.estrellas: self.administrador_eventos.publicar(EventoRecogerEstrella((self.posicion_x, self.posicion_y)))
                if self.vidas > 0 and (self.posicion_x, self.posicion_y) in self.potenciadores:
                    self.potenciadores.remove((self.posicion_x, self.posicion_y))
                    self.administrador_eventos.publicar(EventoPotenciadorRecogido(random.choice([POTENCIADOR_INVULNERABLE, POTENCIADOR_CONGELAR, POTENCIADOR_INVISIBLE])))

                if self.temporizador_potenciador > 0:
                    self.temporizador_potenciador -= 1
                    if self.temporizador_potenciador == 0: self.potenciador_activo = None

                if self.cuadros_mensaje > 0: self.cuadros_mensaje -= 1

                self.controlador_enemigos.actualizar()

                self.vista.limpiar_pantalla(COLOR_FONDO)
                nivel_actual = self.niveles[self.nivel_actual]
                color_pared = tuple(nivel_actual.get("colores", {}).get("pared", COLOR_PARED_DEFAULT))
                color_suelo = tuple(nivel_actual.get("colores", {}).get("suelo", COLOR_SUELO_DEFAULT))
                self.vista.dibujar_laberinto(self.laberinto, self.tamano_celda, color_pared, color_suelo)
                for sx, sy in self.estrellas: self.vista.dibujar_estrella(sx * self.tamano_celda, sy * self.tamano_celda, self.tamano_celda)
                for px, py in self.potenciadores: self.vista.dibujar_potenciador(px * self.tamano_celda, py * self.tamano_celda, self.tamano_celda)
                for ex, ey in self.enemigos: self.vista.dibujar_enemigo(ex * self.tamano_celda, ey * self.tamano_celda, self.tamano_celda)
                self.vista.dibujar_jugador(self.posicion_x * self.tamano_celda, self.posicion_y * self.tamano_celda, self.tamano_celda)
                self.vista.dibujar_texto(f"Estrellas restantes: {len(self.estrellas)}", 20, 20, 24, COLOR_TEXTO_DESTACADO)
                self.vista.dibujar_interfaz(self.vidas, self.puntuacion, x=20, y=self.desplazamiento_interfaz_y)
                if self.mensaje_texto and self.cuadros_mensaje > 0: self.vista.dibujar_texto(self.mensaje_texto, 120, 60, 32, COLOR_TEXTO)
                self.vista.actualizar()
            elif self.estado == ESTADO_MENU:
                self.menu.dibujar(); self.vista.actualizar()
            elif self.estado == ESTADO_GAME_OVER:
                self.vista.limpiar_pantalla((30, 0, 0))
                titulo = "¡Has ganado!" if getattr(self, "_mostrar_victoria", False) else "GAME OVER"
                self.vista.dibujar_texto(titulo, 180 if self._mostrar_victoria else 220, 200, 72, (255, 255, 0) if self._mostrar_victoria else (255, 80, 80))
                self.vista.dibujar_texto(f"Puntaje final: {self.puntuacion_final}", 200, 280, 36, (255, 255, 255))
                self.vista.dibujar_texto("ENTER: Reintentar    ESC: Menú", 160, 340, 28, (220, 220, 220))
                self.vista.actualizar()
            elif self.estado == ESTADO_SALON:
                self.vista.limpiar_pantalla((0, 0, 50))
                self.vista.dibujar_texto("Salón de la Fama", 150, 200, 48, (255, 255, 0))
                ranking = self.gestor_perfiles.obtener_ranking_global(10); y = 270
                if ranking:
                    for i, e in enumerate(ranking[:10]):
                        nombre = e.get('nombre', 'Desconocido'); punt = e.get('puntuacion', 0); fecha = e.get('fecha', '')
                        texto = f"{i+1}. {nombre}: {punt} ({fecha.split()[0] if fecha else ''})"; self.vista.dibujar_texto(texto, 50, y, 20, (255, 255, 255)); y += 25
                else:
                    self.vista.dibujar_texto("No hay puntuaciones registradas", 120, y, 24, (180, 180, 180))
                self.vista.dibujar_texto("ESC: Volver", 120, 580, 32, (200, 200, 200)); self.vista.actualizar()
            elif self.estado == ESTADO_ADMIN:
                self.vista.limpiar_pantalla((50, 0, 0))
                self.vista.dibujar_texto("Administración", 180, 250, 48, (255, 255, 0))
                self.vista.dibujar_texto("ESC: Volver", 120, 350, 32, (200, 200, 200))
                self._recargar_niveles(); self.estado = ESTADO_MENU; self.vista.actualizar()

            self.reloj.tick(self.fps)
