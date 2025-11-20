import pygame
from evento import EventoSeleccionMenu
import json
import os


class MenuPrincipal:
    """Menú principal con sistema de perfiles - 100% Pygame."""

    def __init__(self, vista, administrador_eventos):
        self.vista = vista
        self.administrador_eventos = administrador_eventos
        self.opciones = ["JUEGO", "SALÓN DE LA FAMA", "ADMINISTRACIÓN", "SALIR"]
        self.opciones_subadministracion = [
            "Cargar laberinto",
            "Reiniciar salón",
            "Volver",
        ]
        self.en_subadministracion = False
        self.indice_submenu = 0
        self.indice_principal = 0
        self.usuario_actual = None
        self.archivo_perfiles = "perfiles.json"
        self.pantalla_ingreso_usuario = False
        self.nombre_ingresado = ""
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        self.fuente_pequeña = pygame.font.SysFont(None, 24)
        self.cursor_visible = True
        self.contador_parpadeo = 0

        self._inicializar_perfiles()

    def _inicializar_perfiles(self):
        """Crea archivo de perfiles si no existe."""
        if not os.path.exists(self.archivo_perfiles):
            with open(self.archivo_perfiles, "w", encoding="utf-8") as f:
                json.dump({"usuarios": []}, f, ensure_ascii=False, indent=4)

    def _cargar_perfiles(self):
        """Carga perfiles registrados."""
        try:
            with open(self.archivo_perfiles, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("usuarios", [])
        except:
            return []

    def _guardar_perfiles(self, usuarios):
        """Guarda perfiles en archivo."""
        with open(self.archivo_perfiles, "w", encoding="utf-8") as f:
            json.dump({"usuarios": usuarios}, f, ensure_ascii=False, indent=4)

    def _normalizar_nombre(self, nombre):
        """Normaliza nombre a mayúsculas."""
        return nombre.strip().upper()

    def _usuario_existe(self, nombre_normalizado):
        """Verifica si usuario existe."""
        usuarios = self._cargar_perfiles()
        return any(u["nombre"] == nombre_normalizado for u in usuarios)

    def _crear_nuevo_usuario(self, nombre):
        """Crea nuevo usuario."""
        nombre_normalizado = self._normalizar_nombre(nombre)

        if self._usuario_existe(nombre_normalizado):
            return False

        usuarios = self._cargar_perfiles()
        nuevo_usuario = {
            "nombre": nombre_normalizado,
            "puntuacion_maxima": 0,
            "partidas_jugadas": 0,
        }
        usuarios.append(nuevo_usuario)
        self._guardar_perfiles(usuarios)
        return True

    def seleccionar_usuario(self):
        """Mostrar pantalla de selección/creación de usuario."""
        self.pantalla_ingreso_usuario = True
        self.nombre_ingresado = ""

    def manejar_eventos_usuario(self, evento):
        """Maneja eventos del teclado para ingreso de usuario."""
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                self.pantalla_ingreso_usuario = False
                self.nombre_ingresado = ""
            elif evento.key == pygame.K_RETURN:
                if self.nombre_ingresado.strip():
                    nombre_normalizado = self._normalizar_nombre(self.nombre_ingresado)

                    if not self._usuario_existe(nombre_normalizado):
                        self._crear_nuevo_usuario(self.nombre_ingresado)

                    self.usuario_actual = nombre_normalizado
                    self.pantalla_ingreso_usuario = False
                    self.nombre_ingresado = ""
            elif evento.key == pygame.K_BACKSPACE:
                self.nombre_ingresado = self.nombre_ingresado[:-1]
            else:
                if len(self.nombre_ingresado) < 20:
                    self.nombre_ingresado += evento.unicode

    def dibujar_pantalla_ingreso_usuario(self):
        """Dibuja pantalla de ingreso de usuario."""
        # Fondo
        self.vista.pantalla.fill((50, 50, 50))

        # Título
        titulo = self.fuente_titulo.render("NUEVO USUARIO", True, (0, 255, 0))
        self.vista.pantalla.blit(titulo, (320, 100))

        # Instrucción
        instruccion = self.fuente_pequeña.render(
            "Ingresa tu nombre (será convertido a MAYÚSCULAS):", True, (200, 200, 200)
        )
        self.vista.pantalla.blit(instruccion, (250, 250))

        # Cuadro de texto
        self.contador_parpadeo = (self.contador_parpadeo + 1) % 30
        self.cursor_visible = self.contador_parpadeo < 15

        texto_input = self.nombre_ingresado
        if self.cursor_visible:
            texto_input += "|"

        texto_renderizado = self.fuente_opcion.render(texto_input, True, (255, 255, 0))
        pygame.draw.rect(self.vista.pantalla, (255, 255, 255), (250, 320, 400, 50), 2)
        self.vista.pantalla.blit(texto_renderizado, (260, 325))

        # Instrucciones
        instruccion2 = self.fuente_pequeña.render(
            "Presiona ENTER para continuar | ESC para cancelar", True, (150, 150, 150)
        )
        self.vista.pantalla.blit(instruccion2, (220, 450))

        # Mostrar nombre normalizado
        nombre_normalizado = self._normalizar_nombre(self.nombre_ingresado)
        vista_previa = self.fuente_pequeña.render(
            f"Se mostrará como: {nombre_normalizado}", True, (100, 200, 255)
        )
        self.vista.pantalla.blit(vista_previa, (300, 500))

    def manejar_eventos(self, evento):
        """Maneja eventos del menú."""
        if self.pantalla_ingreso_usuario:
            self.manejar_eventos_usuario(evento)
        else:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    if self.en_subadministracion:
                        self.indice_submenu = (self.indice_submenu - 1) % len(
                            self.opciones_subadministracion
                        )
                    else:
                        self.indice_principal = (self.indice_principal - 1) % len(
                            self.opciones
                        )

                elif evento.key == pygame.K_DOWN:
                    if self.en_subadministracion:
                        self.indice_submenu = (self.indice_submenu + 1) % len(
                            self.opciones_subadministracion
                        )
                    else:
                        self.indice_principal = (self.indice_principal + 1) % len(
                            self.opciones
                        )

                elif evento.key == pygame.K_RETURN:
                    if self.en_subadministracion:
                        self._procesar_opcion_admin(self.indice_submenu)
                    else:
                        if (
                            self.usuario_actual is None
                            and self.indice_principal != len(self.opciones) - 1
                        ):
                            self.seleccionar_usuario()
                        else:
                            self._procesar_opcion_principal(self.indice_principal)

    def _procesar_opcion_principal(self, indice):
        """Procesa opción principal seleccionada."""
        if indice == 0:  # JUEGO
            evento = EventoSeleccionMenu("JUEGO", self.usuario_actual)
            self.administrador_eventos.registrar(evento)
        elif indice == 1:  # SALÓN DE LA FAMA
            evento = EventoSeleccionMenu("SALON_DE_LA_FAMA", None)
            self.administrador_eventos.registrar(evento)
        elif indice == 2:  # ADMINISTRACIÓN
            self.en_subadministracion = True
            self.indice_submenu = 0
        elif indice == 3:  # SALIR
            evento = EventoSeleccionMenu("SALIR", None)
            self.administrador_eventos.registrar(evento)

    def _procesar_opcion_admin(self, indice):
        """Procesa opción de administración."""
        if indice == 0:  # Cargar laberinto
            evento = EventoSeleccionMenu("CARGAR_LABERINTO", None)
            self.administrador_eventos.registrar(evento)
        elif indice == 1:  # Reiniciar salón
            evento = EventoSeleccionMenu("REINICIAR_SALON", None)
            self.administrador_eventos.registrar(evento)
        elif indice == 2:  # Volver
            self.en_subadministracion = False
            self.indice_principal = 0

    def dibujar(self):
        """Dibuja el menú principal."""
        if self.pantalla_ingreso_usuario:
            self.dibujar_pantalla_ingreso_usuario()
        else:
            self.vista.pantalla.fill((0, 0, 0))

            # Título
            titulo = self.fuente_titulo.render("JUEGO RUNNER", True, (0, 255, 0))
            self.vista.pantalla.blit(titulo, (350, 50))

            # Usuario actual
            if self.usuario_actual:
                usuario_texto = self.fuente_pequeña.render(
                    f"Usuario: {self.usuario_actual}", True, (100, 200, 255)
                )
                self.vista.pantalla.blit(usuario_texto)
