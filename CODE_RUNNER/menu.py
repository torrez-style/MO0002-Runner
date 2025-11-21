import pygame
from evento import EventoSeleccionMenu
import os
import json
from logros import GestorLogros

class MenuPrincipal:
    def __init__(self, vista, administrador_eventos):
        self.vista = vista
        self.administrador_eventos = administrador_eventos
        self.opciones = ["JUEGO", "SALÓN DE LA FAMA", "LOGROS", "ADMINISTRACIÓN", "SALIR"]
        self.opciones_subadministracion = [
            "Crear usuario", "Eliminar usuario", "Listar usuarios",
            "Cargar laberinto", "Reiniciar salón", "Volver"
        ]
        self.en_subadministracion = False
        self.indice_submenu = 0
        self.indice_principal = 0
        self.fuente_titulo= pygame.font.SysFont(None, 48)
        self.fuente_opcion= pygame.font.SysFont(None, 36)
        self.mensaje = None
        self.mensaje_tipo = None
        self.mensaje_tiempo = 0
        self.input_activo = False
        self.texto_input = ""
        self.input_callback = None
        self.listar_usuarios = False
        self.usuarios = self._leer_usuarios()
        # Logros
        self.visualizar_logros = False
        self.logros_usuario = GestorLogros(self.usuarios[0] if self.usuarios else "INVITADO")

    def manejar_eventos(self, evento):
        if self.input_activo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if self.input_callback is not None:
                        self.input_callback(self.texto_input)
                        self.input_activo = False
                        self.texto_input = ""
                        self.input_callback = None
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto_input = self.texto_input[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    self.input_activo = False
                    self.texto_input = ""
                    self.input_callback = None
                else:
                    char = evento.unicode
                    if char.isprintable():
                        self.texto_input += char
            return
        if self.listar_usuarios:
            if evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                self.listar_usuarios = False
            return
        if self.visualizar_logros:
            if evento.type == pygame.KEYDOWN and evento.key in [pygame.K_RETURN, pygame.K_ESCAPE]:
                self.visualizar_logros = False
            return
        if self.en_subadministracion:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.indice_submenu = (self.indice_submenu - 1) % len(self.opciones_subadministracion)
                elif evento.key == pygame.K_DOWN:
                    self.indice_submenu = (self.indice_submenu + 1) % len(self.opciones_subadministracion)
                elif evento.key == pygame.K_RETURN:
                    opcion_seleccionada = self.opciones_subadministracion[self.indice_submenu]
                    if opcion_seleccionada == "Crear usuario":
                        self._iniciar_input("Nombre del usuario a crear", self._crear_usuario)
                    elif opcion_seleccionada == "Eliminar usuario":
                        self._iniciar_input("Nombre del usuario a eliminar", self._eliminar_usuario)
                    elif opcion_seleccionada == "Listar usuarios":
                        self.listar_usuarios = True
                    elif opcion_seleccionada == "Cargar laberinto":
                        self._iniciar_input("Ruta del archivo de laberinto (JSON)", self._cargar_laberinto)
                    elif opcion_seleccionada == "Reiniciar salón":
                        self._reiniciar_salon_fama()
                    elif opcion_seleccionada == "Volver":
                        self.en_subadministracion = False
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.indice_principal = (self.indice_principal - 1) % len(self.opciones)
                elif evento.key == pygame.K_DOWN:
                    self.indice_principal = (self.indice_principal + 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    opcion = self.opciones[self.indice_principal]
                    if opcion == "ADMINISTRACIÓN":
                        self.en_subadministracion = True
                        self.indice_submenu = 0
                    elif opcion == "JUEGO":
                        if self._verificar_laberintos_disponibles():
                            self.administrador_eventos.publicar(EventoSeleccionMenu("JUEGO"))
                        else:
                            self._mostrar_mensaje("No hay laberintos cargados. Ve a ADMINISTRACIÓN y carga un archivo.", "warning")
                    elif opcion == "SALÓN DE LA FAMA":
                        self.administrador_eventos.publicar(EventoSeleccionMenu("SALÓN_DE_LA_FAMA"))
                    elif opcion == "LOGROS":
                        self.visualizar_logros = True
                    elif opcion == "SALIR":
                        self.administrador_eventos.publicar(EventoSeleccionMenu("SALIR"))

    def _iniciar_input(self, mensaje, callback):
        self.input_activo = True
        self.texto_input = ""
        self.input_callback = callback
        self.mensaje = mensaje
        self.mensaje_tipo = "info"
        self.mensaje_tiempo = 0

    def dibujar(self):
        self.vista.limpiar_pantalla((0, 0, 0))
        superficie_titulo = self.fuente_titulo.render("Maze-Run", True, (255, 255, 255))
        x_titulo = (self.vista.ancho - superficie_titulo.get_width()) // 2
        self.vista.pantalla.blit(superficie_titulo, (x_titulo, 100))
        if self.input_activo:
            self._dibujar_input()
        elif self.listar_usuarios:
            self._dibujar_lista_usuarios()
        elif self.visualizar_logros:
            self._dibujar_logros_usuario()
        elif self.mensaje:
            self._dibujar_mensaje(self.mensaje, self.mensaje_tipo)
        elif self.en_subadministracion:
            for indice, opcion in enumerate(self.opciones_subadministracion):
                color = (255, 255, 0) if indice == self.indice_submenu else (200, 200, 200)
                superficie = self.fuente_opcion.render(opcion, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
                self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))
        else:
            for indice, opcion in enumerate(self.opciones):
                color = (255, 255, 0) if indice == self.indice_principal else (200, 200, 200)
                superficie = self.fuente_opcion.render(opcion, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
                self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))

    def _dibujar_input(self):
        fondo = pygame.Surface((520, 150))
        fondo.fill((35, 35, 35))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho//2, self.vista.alto//2)
        self.vista.pantalla.blit(fondo, rect)
        fuente = pygame.font.SysFont(None, 32)
        pregunta = fuente.render(self.mensaje, True, (255, 255, 255))
        self.vista.pantalla.blit(pregunta, (rect.left+30, rect.top+30))
        entrada = fuente.render(self.texto_input, True, (200, 255, 200))
        self.vista.pantalla.blit(entrada, (rect.left+30, rect.top+70))
        instruccion = fuente.render("ENTER: Confirmar | ESC: Cancelar", True, (180, 180, 180))
        self.vista.pantalla.blit(instruccion, (rect.left+30, rect.top+110))

    def _dibujar_lista_usuarios(self):
        fondo = pygame.Surface((520, 350))
        fondo.fill((42, 42, 52))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho//2, self.vista.alto//2)
        self.vista.pantalla.blit(fondo, rect)
        fuente = pygame.font.SysFont(None, 32)
        titulo = fuente.render("Usuarios existentes:", True, (255, 255, 255))
        self.vista.pantalla.blit(titulo, (rect.left+30, rect.top+30))
        y = rect.top+70
        for usuario in self.usuarios:
            texto = fuente.render(usuario, True, (200, 255, 255))
            self.vista.pantalla.blit(texto, (rect.left+30, y))
            y += 30
        msg = fuente.render("ENTER/ESC para volver", True, (180,180,180))
        self.vista.pantalla.blit(msg, (rect.left+30, rect.bottom-50))

    def _dibujar_logros_usuario(self):
        fondo = pygame.Surface((520, 350))
        fondo.fill((20, 40, 30))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho//2, self.vista.alto//2)
        self.vista.pantalla.blit(fondo, rect)
        fuente = pygame.font.SysFont(None, 32)
        titulo = fuente.render(f"Logros de {self.logros_usuario.usuario}:", True, (255, 255, 200))
        self.vista.pantalla.blit(titulo, (rect.left+30, rect.top+30))
        y = rect.top+70
        logros = self.logros_usuario.logros.values()
        for logro in logros:
            estado = "✓" if logro.desbloqueado else "✗"
            texto = fuente.render(f"{estado} {logro.icono} {logro.nombre}: {logro.descripcion}", True, (150 if logro.desbloqueado else 255, 255, 100))
            self.vista.pantalla.blit(texto, (rect.left+30, y))
            y += 36
        msg = fuente.render("ENTER/ESC para volver", True, (200,200,200))
        self.vista.pantalla.blit(msg, (rect.left+30, rect.bottom-50))

    def _dibujar_mensaje(self, texto, tipo="info"):
        color = (255, 255, 255)
        if tipo == "warning":
            color = (255, 255, 0)
        elif tipo == "error":
            color = (255, 64, 64)
        fuente = pygame.font.SysFont(None, 32)
        mensaje = fuente.render(texto, True, color)
        rect = mensaje.get_rect()
        rect.center = (self.vista.ancho//2, 550)
        self.vista.pantalla.blit(mensaje, rect)
        self.mensaje_tiempo += 1
        if self.mensaje_tiempo > 180:
            self.mensaje = None
            self.mensaje_tiempo = 0
            self.mensaje_tipo = None

    def _mostrar_mensaje(self, texto, tipo="info"):
        self.mensaje = texto
        self.mensaje_tipo = tipo
        self.mensaje_tiempo = 0

    def _leer_usuarios(self):
        try:
            with open("CODE_RUNNER/perfiles.json", "r", encoding="utf-8") as archivo:
                lista = json.load(archivo)
            lista = [x.upper() for x in lista if isinstance(x, str)]
            return sorted(set(lista))
        except Exception:
            return []

    def _guardar_usuarios(self):
        with open("CODE_RUNNER/perfiles.json", "w", encoding="utf-8") as archivo:
            json.dump(sorted(set(self.usuarios)), archivo, indent=2, ensure_ascii=False)

    def _crear_usuario(self, nombre):
        nombre = nombre.strip().upper()
        if not nombre:
            self._mostrar_mensaje("Nombre de usuario vacío o inválido.", "error")
            return
        if nombre in self.usuarios:
            self._mostrar_mensaje(f"El usuario '{nombre}' ya existe.", "error")
            return
        self.usuarios.append(nombre)
        self._guardar_usuarios()
        self._mostrar_mensaje(f"Usuario '{nombre}' creado correctamente.", "info")
        # Actualizar gestor de logros al crear usuario
        self.logros_usuario = GestorLogros(nombre)

    def _eliminar_usuario(self, nombre):
        nombre = nombre.strip().upper()
        if nombre not in self.usuarios:
            self._mostrar_mensaje(f"El usuario '{nombre}' no existe.", "error")
            return
        self.usuarios = [u for u in self.usuarios if u != nombre]
        self._guardar_usuarios()
        self._mostrar_mensaje(f"Usuario '{nombre}' eliminado correctamente.", "info")
        # Si borras usuario logros, actualiza a invitado
        if self.logros_usuario.usuario == nombre:
            self.logros_usuario = GestorLogros("INVITADO")

    def _verificar_laberintos_disponibles(self):
        try:
            ruta = "niveles.json" if os.path.exists("niveles.json") else "CODE_RUNNER/niveles.json"
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return "niveles" in datos and isinstance(datos["niveles"], list) and len(datos["niveles"]) > 0
        except Exception:
            return False

    def _cargar_laberinto(self, ruta_json):
        if not ruta_json or not os.path.exists(ruta_json):
            self._mostrar_mensaje("No se encontró el archivo especificado.", "error")
            return
        try:
            with open(ruta_json, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            if self._validar_estructura_laberinto(datos):
                with open("niveles.json", "w", encoding="utf-8") as archivo_salida:
                    json.dump(datos, archivo_salida, indent=2, ensure_ascii=False)
                self._mostrar_mensaje(f"Se cargaron {len(datos['niveles'])} laberinto(s) correctamente.", "info")
            else:
                self._mostrar_mensaje("Formato incorrecto. Requiere clave 'niveles', matriz rectangular y valores válidos.", "error")
        except json.JSONDecodeError:
            self._mostrar_mensaje("El archivo seleccionado no es JSON válido.", "error")
        except Exception as excepcion:
            self._mostrar_mensaje(f"Error: {excepcion}", "error")

    def _validar_estructura_laberinto(self, datos):
        try:
            if not isinstance(datos, dict) or "niveles" not in datos:
                return False
            niveles = datos["niveles"]
            if not isinstance(niveles, list) or len(niveles) == 0:
                return False
            for nivel in niveles:
                if not isinstance(nivel, dict):
                    return False
                for campo in ["nombre", "laberinto", "entrada", "salida"]:
                    if campo not in nivel:
                        return False
                laberinto=nivel["laberinto"]
                if not isinstance(laberinto, list) or len(laberinto) == 0:
                    return False
                ancho=len(laberinto[0])
                for fila in laberinto:
                    if not isinstance(fila, list) or len(fila) != ancho:
                        return False
                    for celda in fila:
                        if not isinstance(celda, int) or celda not in [0,1,2,3]:
                            return False
                entrada = nivel["entrada"]
                salida = nivel["salida"]
                if (not isinstance(entrada, list) or len(entrada) != 2 or not isinstance(salida, list) or len(salida) != 2):
                    return False
            return True
        except Exception:
            return False

    def _reiniciar_salon_fama(self):
        try:
            with open("puntuaciones.json", "w", encoding="utf-8") as archivo:
                json.dump([], archivo)
            self._mostrar_mensaje("El salón de la fama ha sido vaciado correctamente.", "info")
        except Exception as excepcion:
            self._mostrar_mensaje(f"Error al vaciar el salón de la fama: {excepcion}", "error")
