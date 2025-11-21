import pygame
import json
from evento import EventoSeleccionMenu
from salon_de_la_fama import SalonDeLaFama

class MenuPrincipal:
    def __init__(self, vista, administrador_eventos):
        self.vista = vista
        self.administrador_eventos = administrador_eventos
        self.opciones = ["JUEGO", "SALÓN DE LA FAMA", "ADMINISTRACIÓN", "SALIR"]
        self.opciones_subadministracion = [
            "Crear usuario",
            "Eliminar usuario",
            "Listar usuarios",
            "Reiniciar salón",
            "Volver",
        ]
        self.en_subadministracion = False
        self.indice_submenu = 0
        self.indice_principal = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        self.mensaje = None
        self.mensaje_tipo = None
        self.mensaje_tiempo = 0
        self.input_activo = False
        self.texto_input = ""
        self.input_callback = None
        self.listar_usuarios = False
        self.usuarios = self._leer_usuarios()
        self.salon = SalonDeLaFama()
        self.mostrar_salon = False
        self.usuario_actual = None
        # Nuevas variables para proceso de eliminación
        self.eliminar_en_progreso = False
        self.usuario_a_eliminar = None
        self.pide_contraseña = False
        self.PASSWORD_ADMIN = "admin2025"

    def manejar_eventos(self, evento):
        if self.input_activo:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    if self.input_callback is not None:
                        self.input_callback(self.texto_input)
                    self.input_activo = False
                    self.texto_input = ""
                    self.input_callback = None
                    self.pide_contraseña = False
                elif evento.key == pygame.K_BACKSPACE:
                    self.texto_input = self.texto_input[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    self.input_activo = False
                    self.texto_input = ""
                    self.input_callback = None
                    self.pide_contraseña = False
                    self.usuario_a_eliminar = None
                else:
                    char = evento.unicode
                    if char.isprintable():
                        self.texto_input += char
            return

        if self.en_subadministracion:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.indice_submenu = (self.indice_submenu - 1) % len(
                        self.opciones_subadministracion
                    )
                elif evento.key == pygame.K_DOWN:
                    self.indice_submenu = (self.indice_submenu + 1) % len(
                        self.opciones_subadministracion
                    )
                elif evento.key == pygame.K_RETURN:
                    opcion_seleccionada = self.opciones_subadministracion[
                        self.indice_submenu
                    ]
                    if opcion_seleccionada == "Crear usuario":
                        self._iniciar_input(
                            "Nombre del usuario a crear", self._crear_usuario
                        )
                    elif opcion_seleccionada == "Eliminar usuario":
                        self.eliminar_en_progreso = True
                        self._iniciar_input(
                            "Nombre del usuario a eliminar", self._fi_eliminacion_usuario
                        )
                    elif opcion_seleccionada == "Listar usuarios":
                        self.listar_usuarios = True
                    elif opcion_seleccionada == "Reiniciar salón":
                        self._reiniciar_salon_fama()
                    elif opcion_seleccionada == "Volver":
                        self.en_subadministracion = False
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.indice_principal = (self.indice_principal - 1) % len(
                        self.opciones
                    )
                elif evento.key == pygame.K_DOWN:
                    self.indice_principal = (self.indice_principal + 1) % len(
                        self.opciones
                    )
                elif evento.key == pygame.K_RETURN:
                    opcion = self.opciones[self.indice_principal]
                    if opcion == "ADMINISTRACIÓN":
                        self.en_subadministracion = True
                        self.indice_submenu = 0
                    elif opcion == "JUEGO":
                        self.administrador_eventos.publicar(
                            EventoSeleccionMenu("JUEGO")
                        )
                    elif opcion == "SALÓN DE LA FAMA":
                        self.mostrar_salon = True
                    elif opcion == "SALIR":
                        self.administrador_eventos.publicar(
                            EventoSeleccionMenu("SALIR")
                        )

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
        elif self.mostrar_salon:
            self._dibujar_salon_fama()
        elif self.listar_usuarios:
            self._dibujar_lista_usuarios()
        elif self.mensaje:
            self._dibujar_mensaje(self.mensaje, self.mensaje_tipo)
        elif self.en_subadministracion:
            for indice, opcion in enumerate(self.opciones_subadministracion):
                color = (
                    (255, 255, 0) if indice == self.indice_submenu else (200, 200, 200)
                )
                superficie = self.fuente_opcion.render(opcion, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
                self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))
        else:
            for indice, opcion in enumerate(self.opciones):
                color = (
                    (255, 255, 0)
                    if indice == self.indice_principal
                    else (200, 200, 200)
                )
                superficie = self.fuente_opcion.render(opcion, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
                self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))

    def _dibujar_input(self):
        fondo = pygame.Surface((520, 150))
        fondo.fill((35, 35, 35))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho // 2, self.vista.alto // 2)
        self.vista.pantalla.blit(fondo, rect)

        fuente = pygame.font.SysFont(None, 32)
        pregunta = fuente.render(self.mensaje, True, (255, 255, 255))
        self.vista.pantalla.blit(pregunta, (rect.left + 30, rect.top + 30))

        # Ocultar la contraseña con asteriscos si estamos en el segundo paso
        texto_a_mostrar = self.texto_input
        if self.pide_contraseña:
            texto_a_mostrar = "*" * len(self.texto_input)
        entrada = fuente.render(texto_a_mostrar, True, (200, 255, 200))
        self.vista.pantalla.blit(entrada, (rect.left + 30, rect.top + 70))

        instruccion = fuente.render(
            "ENTER: Confirmar | ESC: Cancelar", True, (180, 180, 180)
        )
        self.vista.pantalla.blit(instruccion, (rect.left + 30, rect.top + 110))

    def _dibujar_salon_fama(self):
        fondo = pygame.Surface((700, 450))
        fondo.fill((42, 42, 52))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho // 2, self.vista.alto // 2)
        self.vista.pantalla.blit(fondo, rect)

        fuente_titulo = pygame.font.SysFont(None, 40)
        fuente_texto = pygame.font.SysFont(None, 28)

        titulo = fuente_titulo.render("SALÓN DE LA FAMA", True, (255, 215, 0))
        self.vista.pantalla.blit(titulo, (rect.left + 150, rect.top + 20))

        ranking = self.salon.obtener_ranking_global(10)

        y_pos = rect.top + 70
        if ranking:
            for idx, entrada in enumerate(ranking, 1):
                texto = f"{idx}. {entrada['usuario']} - {entrada['puntuacion']} pts"
                surf = fuente_texto.render(texto, True, (200, 255, 200))
                self.vista.pantalla.blit(surf, (rect.left + 30, y_pos))
                y_pos += 30
        else:
            sin_datos = fuente_texto.render("Sin datos aún", True, (200, 200, 200))
            self.vista.pantalla.blit(sin_datos, (rect.left + 30, y_pos))

        instruccion = fuente_texto.render("ENTER/ESC: Volver", True, (180, 180, 180))
        self.vista.pantalla.blit(instruccion, (rect.left + 30, rect.bottom - 40))

    def _dibujar_lista_usuarios(self):
        fondo = pygame.Surface((520, 350))
        fondo.fill((42, 42, 52))
        rect = fondo.get_rect()
        rect.center = (self.vista.ancho // 2, self.vista.alto // 2)
        self.vista.pantalla.blit(fondo, rect)

        fuente = pygame.font.SysFont(None, 32)
        titulo = fuente.render("Usuarios existentes:", True, (255, 255, 255))
        self.vista.pantalla.blit(titulo, (rect.left + 30, rect.top + 30))

        y = rect.top + 70
        for usuario in self.usuarios:
            texto = fuente.render(usuario, True, (200, 255, 255))
            self.vista.pantalla.blit(texto, (rect.left + 30, y))
            y += 30

        msg = fuente.render("ENTER/ESC para volver", True, (180, 180, 180))
        self.vista.pantalla.blit(msg, (rect.left + 30, rect.bottom - 50))

    def _dibujar_mensaje(self, texto, tipo="info"):
        color = (255, 255, 255)
        if tipo == "warning":
            color = (255, 255, 0)
        elif tipo == "error":
            color = (255, 64, 64)

        fuente = pygame.font.SysFont(None, 32)
        mensaje = fuente.render(texto, True, color)
        rect = mensaje.get_rect()
        rect.center = (self.vista.ancho // 2, 550)
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

    def _fi_eliminacion_usuario(self, nombre):
        nombre = nombre.strip().upper()
        if nombre not in self.usuarios:
            self._mostrar_mensaje(f"El usuario '{nombre}' no existe.", "error")
            self.eliminar_en_progreso = False
            self.usuario_a_eliminar = None
            return
        self.usuario_a_eliminar = nombre
        self.pide_contraseña = True
        self._iniciar_input(
            f"Ingrese contraseña para eliminar '{nombre}'", self._verificar_password_y_eliminar
        )

    def _verificar_password_y_eliminar(self, password):
        if self.usuario_a_eliminar is None:
            self._mostrar_mensaje("Error: No hay usuario seleccionado.", "error")
            self.eliminar_en_progreso = False
            self.pide_contraseña = False
            return
        if password.strip() != self.PASSWORD_ADMIN:
            self._mostrar_mensaje("Contraseña incorrecta. Eliminación cancelada.", "error")
            self.eliminar_en_progreso = False
            self.pide_contraseña = False
            self.usuario_a_eliminar = None
            return
        # Contraseña correcta, eliminar usuario
        nombre = self.usuario_a_eliminar
        self.usuarios = [u for u in self.usuarios if u != nombre]
        self._guardar_usuarios()
        self._mostrar_mensaje(f"Usuario '{nombre}' eliminado correctamente.", "info")
        self.eliminar_en_progreso = False
        self.pide_contraseña = False
        self.usuario_a_eliminar = None

    def _reiniciar_salon_fama(self):
        try:
            with open("puntuaciones.json", "w", encoding="utf-8") as archivo:
                json.dump({}, archivo)
            self._mostrar_mensaje(
                "El salón de la fama ha sido vaciado correctamente.", "info"
            )
        except Exception as excepcion:
            self._mostrar_mensaje(
                f"Error al vaciar el salón de la fama: {excepcion}", "error"
            )
