import os
import json
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pygame
from evento import EventoSeleccionMenu

# Claves internas del estado/menú (sin tildes)
OPCION_JUEGO = "JUEGO"
OPCION_SALON = "SALON_DE_LA_FAMA"
OPCION_ADMIN = "ADMINISTRACION"
OPCION_SALIR = "SALIR"

class MenuPrincipal:
    def __init__(self, vista, administrador_eventos):
        self.vista = vista
        self.administrador_eventos = administrador_eventos
        # Texto mostrado puede llevar tildes, claves internas no
        self.opciones = [OPCION_JUEGO, OPCION_SALON, OPCION_ADMIN, OPCION_SALIR]
        self.opciones_subadministracion = ["Cargar laberinto", "Reiniciar salon", "Volver"]
        self.en_subadministracion = False
        self.indice_submenu = 0
        self.indice_principal = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        # Mover credencial a variable de entorno si se desea
        self.contrasena_administrador = os.getenv("GAME_ADMIN_PASS", "admin2025")

    def manejar_eventos(self, evento):
        if self.en_subadministracion:
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
                    if opcion == OPCION_ADMIN:
                        if self._autenticar_administrador():
                            self.en_subadministracion = True
                            self.indice_submenu = 0
                    elif opcion == OPCION_JUEGO:
                        if self._verificar_laberintos_disponibles():
                            self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_JUEGO))
                        else:
                            self._mostrar_mensaje_sin_laberintos()
                    elif opcion == OPCION_SALON:
                        self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_SALON))
                    elif opcion == OPCION_SALIR:
                        self.administrador_eventos.publicar(EventoSeleccionMenu(OPCION_SALIR))

    def _autenticar_administrador(self):
        # En entornos sin tkinter, capturar excepciones
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
        self.vista.pantalla.blit(superficie_titulo, (x_titulo, 100))

        if self.en_subadministracion:
            for indice, opcion in enumerate(self.opciones_subadministracion):
                color = (255, 255, 0) if indice == self.indice_submenu else (200, 200, 200)
                superficie = self.fuente_opcion.render(opcion, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
                self.vista.pantalla.blit(superficie, (x_opcion, y_opcion))
        else:
            for indice, opcion in enumerate(self.opciones):
                # Mostrar con tildes donde aplica
                etiqueta = {
                    OPCION_JUEGO: "JUEGO",
                    OPCION_SALON: "SALÓN DE LA FAMA",
                    OPCION_ADMIN: "ADMINISTRACIÓN",
                    OPCION_SALIR: "SALIR",
                }[opcion]
                color = (255, 255, 0) if indice == self.indice_principal else (200, 200, 200)
                superficie = self.fuente_opcion.render(etiqueta, True, color)
                x_opcion = (self.vista.ancho - superficie.get_width()) // 2
                y_opcion = 200 + indice * 50
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
                    with open("niveles.json", "w", encoding="utf-8") as archivo_salida:
                        json.dump(datos, archivo_salida, indent=2, ensure_ascii=False)
                    messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(datos['niveles'])} laberinto(s) correctamente.\n\nYa puede jugar desde el menú principal.")
                else:
                    messagebox.showerror("Error de Validación", "El archivo no tiene el formato correcto.\n\nRequisitos:\n- Debe tener clave 'niveles'\n- Cada nivel debe tener: nombre, laberinto (matriz), entrada, salida\n- La matriz debe ser rectangular con valores válidos")
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
                entrada = nivel["entrada"]; salida = nivel["salida"]
                if (not isinstance(entrada, list) or len(entrada) != 2 or
                    not isinstance(salida, list) or len(salida) != 2):
                    return False
            return True
        except Exception:
            return False

    def _reiniciar_salon_fama(self):
        try:
            with open("puntuaciones.json", "w", encoding="utf-8") as archivo:
                json.dump([], archivo)
            messagebox.showinfo("Reinicio Exitoso", "El salón de la fama ha sido vaciado correctamente.")
        except Exception as excepcion:
            messagebox.showerror("Error", f"No se pudo vaciar el salón de la fama:\n{excepcion}")
