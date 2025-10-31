import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pygame
from evento import EventoSeleccionMenu
from constantes import ESTADO_MENU, ESTADO_JUEGO, ESTADO_SALON, ESTADO_ADMIN, ESTADO_GAME_OVER
from gestor_perfiles import GestorPerfiles

# Claves internas del estado/menú (usar constantes compartidas)
OPCION_JUEGO = ESTADO_JUEGO
OPCION_SALON = ESTADO_SALON
OPCION_ADMIN = ESTADO_ADMIN
OPCION_PERFILES = "PERFILES"
OPCION_SALIR = "SALIR"

class MenuPrincipal:
    def __init__(self, vista, administrador_eventos):
        self.vista = vista
        self.administrador_eventos = administrador_eventos
        self.opciones = [OPCION_JUEGO, OPCION_PERFILES, OPCION_SALON, OPCION_ADMIN, OPCION_SALIR]
        self.opciones_subadministracion = ["Cargar laberinto", "Reiniciar salon", "Gestionar perfiles", "Volver"]
        self.opciones_perfiles = ["Seleccionar perfil", "Crear perfil", "Eliminar perfil", "Volver"]
        self.en_subadministracion = False
        self.en_perfiles = False
        self.indice_submenu = 0
        self.indice_perfiles = 0
        self.indice_principal = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        self.fuente_info = pygame.font.SysFont(None, 24)
        self.contrasena_administrador = os.getenv("GAME_ADMIN_PASS", "admin2025")
        self.gestor_perfiles = GestorPerfiles()
        self._asegurar_perfil_inicial()

    def _asegurar_perfil_inicial(self):
        """Asegura que exista al menos un perfil y selecciona uno por defecto."""
        perfiles = self.gestor_perfiles.cargar_perfiles()
        if not perfiles:
            self.gestor_perfiles.crear_perfil("Jugador1")
            perfiles = self.gestor_perfiles.cargar_perfiles()
        if perfiles and not self.gestor_perfiles.obtener_perfil_activo():
            self.gestor_perfiles.seleccionar_perfil(perfiles[0]['id'])

    def manejar_eventos(self, evento):
        if self.en_perfiles:
            self._manejar_eventos_perfiles(evento)
        elif self.en_subadministracion:
            self._manejar_eventos_admin(evento)
        else:
            self._manejar_eventos_principal(evento)

    def _manejar_eventos_perfiles(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_perfiles = (self.indice_perfiles - 1) % len(self.opciones_perfiles)
            elif evento.key == pygame.K_DOWN:
                self.indice_perfiles = (self.indice_perfiles + 1) % len(self.opciones_perfiles)
            elif evento.key == pygame.K_RETURN:
                opcion = self.opciones_perfiles[self.indice_perfiles]
                if opcion == "Seleccionar perfil":
                    self._seleccionar_perfil()
                elif opcion == "Crear perfil":
                    self._crear_perfil()
                elif opcion == "Eliminar perfil":
                    self._eliminar_perfil()
                elif opcion == "Volver":
                    self.en_perfiles = False

    def _manejar_eventos_admin(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_submenu = (self.indice_submenu - 1) % len(self.opciones_subadministracion)
            elif evento.key == pygame.K_DOWN:
                self.indice_submenu = (self.indice_submenu + 1) % len(self.opciones_subadministracion)
            elif evento.key == pygame.K_RETURN:
                opcion_seleccionada = self.opciones_subadministracion[self.indice_submenu]
                if opcion_seleccionada == "Cargar laberinto":
                    self._cargar_laberinto()
                elif opcion_seleccionada == "Reiniciar salon":
                    self._reiniciar_salon_fama()
                elif opcion_seleccionada == "Gestionar perfiles":
                    self.en_subadministracion = False
                    self.en_perfiles = True
                elif opcion_seleccionada == "Volver":
                    self.en_subadministracion = False

    def _manejar_eventos_principal(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP:
                self.indice_principal = (self.indice_principal - 1) % len(self.opciones)
            elif evento.key == pygame.K_DOWN:
                self.indice_principal = (self.indice_principal + 1) % len(self.opciones)
            elif evento.key == pygame.K_RETURN:
                opcion = self.opciones[self.indice_principal]
                if opcion == OPCION_ADMIN:
                    if self._autenticar_administrador():
                        self.en_subadministracion = True
                        self.indice_submenu = 0
                elif opcion == OPCION_JUEGO:
                    if self._verificar_laberintos_disponibles():
                        self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_JUEGO))
                    else:
                        self._mostrar_mensaje_sin_laberintos()
                elif opcion == OPCION_PERFILES:
                    self.en_perfiles = True
                    self.indice_perfiles = 0
                elif opcion == OPCION_SALON:
                    self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_SALON))
                elif opcion == OPCION_SALIR:
                    self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_SALIR))

    def _seleccionar_perfil(self):
        perfiles = self.gestor_perfiles.cargar_perfiles()
        if not perfiles:
            self._mostrar_mensaje("No hay perfiles creados")
            return
        
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            opciones_texto = "\n".join([f"{p['id']}: {p['nombre']} (Partidas: {p.get('partidas_jugadas', 0)}, Mejor: {p.get('mejor_puntuacion', 0)})" for p in perfiles])
            seleccion = simpledialog.askstring("Seleccionar Perfil", f"Perfiles disponibles:\n{opciones_texto}\n\nIngrese ID del perfil:")
            if seleccion and seleccion.isdigit():
                perfil_id = int(seleccion)
                if self.gestor_perfiles.seleccionar_perfil(perfil_id):
                    messagebox.showinfo("Perfil Seleccionado", f"Perfil '{self.gestor_perfiles.obtener_perfil_activo()['nombre']}' seleccionado")
                else:
                    messagebox.showerror("Error", "Perfil no encontrado")
        finally:
            ventana_raiz.destroy()

    def _crear_perfil(self):
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            nombre = simpledialog.askstring("Crear Perfil", "Ingrese nombre del nuevo perfil:")
            if nombre:
                perfil = self.gestor_perfiles.crear_perfil(nombre)
                if perfil:
                    messagebox.showinfo("Perfil Creado", f"Perfil '{nombre}' creado exitosamente")
                else:
                    messagebox.showerror("Error", "No se pudo crear el perfil (posible nombre duplicado)")
        finally:
            ventana_raiz.destroy()

    def _eliminar_perfil(self):
        perfiles = self.gestor_perfiles.cargar_perfiles()
        if len(perfiles) <= 1:
            self._mostrar_mensaje("Debe existir al menos un perfil")
            return
        
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            opciones_texto = "\n".join([f"{p['id']}: {p['nombre']}" for p in perfiles])
            seleccion = simpledialog.askstring("Eliminar Perfil", f"Perfiles disponibles:\n{opciones_texto}\n\nIngrese ID del perfil a eliminar:")
            if seleccion and seleccion.isdigit():
                perfil_id = int(seleccion)
                if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este perfil y todas sus puntuaciones?"):
                    if self.gestor_perfiles.eliminar_perfil(perfil_id):
                        messagebox.showinfo("Perfil Eliminado", "Perfil eliminado exitosamente")
                        self._asegurar_perfil_inicial()  # Reseleccionar perfil por defecto
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el perfil")
        finally:
            ventana_raiz.destroy()

    def _mostrar_mensaje(self, mensaje):
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            messagebox.showinfo("Información", mensaje)
        finally:
            ventana_raiz.destroy()

    def _autenticar_administrador(self):
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            contrasena_ingresada = simpledialog.askstring("Acceso Administrativo", "Ingrese la contraseña de administrador:", show='*')
            if contrasena_ingresada == self.contrasena_administrador:
                messagebox.showinfo("Acceso Concedido", "Bienvenido al panel administrativo"); return True
            elif contrasena_ingresada is not None:
                messagebox.showerror("Acceso Denegado", "Contraseña incorrecta")
            return False
        except Exception:
            return False
        finally:
            ventana_raiz.destroy()

    def _verificar_laberintos_disponibles(self):
        try:
            ruta = "niveles.json" if os.path.exists("niveles.json") else os.path.join("CODE_RUNNER", "niveles.json")
            with open(ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
                return "niveles" in datos and isinstance(datos["niveles"], list) and len(datos["niveles"]) > 0
        except Exception:
            return False

    def _mostrar_mensaje_sin_laberintos(self):
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        try:
            messagebox.showwarning("Sin Laberintos", "No hay laberintos cargados.\n\nPara jugar, debe:\n1. Ir a ADMINISTRACION\n2. Usar contraseña de administrador\n3. Cargar archivos de laberinto")
        finally:
            ventana_raiz.destroy()

    def dibujar(self):
        self.vista.limpiar_pantalla((0, 0, 0))
        superficie_titulo = self.fuente_titulo.render("Maze-Run", True, (255, 255, 255))
        x_titulo = (self.vista.ancho - superficie_titulo.get_width()) // 2
        self.vista.pantalla.blit(superficie_titulo, (x_titulo, 80))

        # Mostrar perfil activo
        perfil_activo = self.gestor_perfiles.obtener_perfil_activo()
        if perfil_activo:
            info_perfil = f"Jugador: {perfil_activo['nombre']} | Partidas: {perfil_activo.get('partidas_jugadas', 0)} | Mejor: {perfil_activo.get('mejor_puntuacion', 0)}"
            superficie_info = self.fuente_info.render(info_perfil, True, (180, 180, 180))
            x_info = (self.vista.ancho - superficie_info.get_width()) // 2
            self.vista.pantalla.blit(superficie_info, (x_info, 120))

        if self.en_perfiles:
            self._dibujar_menu_perfiles()
        elif self.en_subadministracion:
            self._dibujar_menu_admin()
        else:
            self._dibujar_menu_principal()

    def _dibujar_menu_perfiles(self):
        for indice, opcion in enumerate(self.opciones_perfiles):
            color = (255, 255, 0) if indice == self.indice_perfiles else (200, 200, 200)
            superficie = self.fuente_opcion.render(opcion, True, color)
            x_opcion = (self.vista.ancho - superficie.get_width()) // 2
            y_opcion = 200 + indice * 50
            self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))

    def _dibujar_menu_admin(self):
        for indice, opcion in enumerate(self.opciones_subadministracion):
            color = (255, 255, 0) if indice == self.indice_submenu else (200, 200, 200)
            superficie = self.fuente_opcion.render(opcion, True, color)
            x_opcion = (self.vista.ancho - superficie.get_width()) // 2
            y_opcion = 200 + indice * 50
            self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))

    def _dibujar_menu_principal(self):
        for indice, opcion in enumerate(self.opciones):
            etiqueta = {
                OPCION_JUEGO: "JUEGO",
                OPCION_PERFILES: "PERFILES",
                OPCION_SALON: "SALÓN DE LA FAMA",
                OPCION_ADMIN: "ADMINISTRACIÓN",
                OPCION_SALIR: "SALIR",
            }[opcion]
            color = (255, 255, 0) if indice == self.indice_principal else (200, 200, 200)
            superficie = self.fuente_opcion.render(etiqueta, True, color)
            x_opcion = (self.vista.ancho - superficie.get_width()) // 2
            y_opcion = 170 + indice * 50
            self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))

    def _cargar_laberinto(self):
        ventana_raiz = tk.Tk(); ventana_raiz.withdraw()
        tipos_archivo = [("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        nombre_archivo = filedialog.askopenfilename(title="Seleccionar nuevo laberinto", filetypes=tipos_archivo)
        if nombre_archivo and os.path.exists(nombre_archivo):
            try:
                with open(nombre_archivo, "r", encoding="utf-8") as archivo:
                    datos = json.load(archivo)
                if self._validar_estructura_laberinto(datos):
                    with open("CODE_RUNNER/niveles.json", "w", encoding="utf-8") as archivo_salida:
                        json.dump(datos, archivo_salida, indent=2, ensure_ascii=False)
                    messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(datos['niveles'])} laberinto(s) correctamente.\n\nYa puede jugar desde el menú principal.")
                else:
                    messagebox.showerror("Error de Validación", "El archivo no tiene el formato correcto.")
            except json.JSONDecodeError:
                messagebox.showerror("Error de Formato", "El archivo no es un JSON válido")
            except Exception as excepcion:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{excepcion}")
        ventana_raiz.destroy()

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
                laberinto = nivel["laberinto"]
                if not isinstance(laberinto, list) or len(laberinto) == 0:
                    return False
                ancho = len(laberinto[0])
                for fila in laberinto:
                    if not isinstance(fila, list) or len(fila) != ancho:
                        return False
                    for celda in fila:
                        if not isinstance(celda, int) or celda not in [0, 1, 2, 3]:
                            return False
            return True
        except Exception:
            return False

    def _reiniciar_salon_fama(self):
        try:
            with open("CODE_RUNNER/puntuaciones.json", "w", encoding="utf-8") as archivo:
                json.dump([], archivo)
            messagebox.showinfo("Reinicio Exitoso", "El salón de la fama ha sido vaciado correctamente.")
        except Exception as excepcion:
            messagebox.showerror("Error", f"No se pudo vaciar el salón de la fama:\n{excepcion}")
