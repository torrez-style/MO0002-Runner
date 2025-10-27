import pygame
from evento import EventoSeleccionMenu
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
import json

class MenuPrincipal:
    def __init__(self, vista, evento_mgr):
        self.vista = vista
        self.evento_mgr = evento_mgr
        # Corrección de acento y nombre amigable para español
        self.opciones = ["JUEGO", "SALÓN DE LA FAMA", "ADMINISTRACIÓN", "SALIR"]
        self.admin_subopciones = ["Cargar laberinto", "Reiniciar salón", "Volver"]
        self.en_subadmin = False
        self.subindice = 0
        self.indice = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        self.admin_password = "admin2025"

    def manejar_eventos(self, e):
        if self.en_subadmin:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.subindice = (self.subindice - 1) % len(self.admin_subopciones)
                elif e.key == pygame.K_DOWN:
                    self.subindice = (self.subindice + 1) % len(self.admin_subopciones)
                elif e.key == pygame.K_RETURN:
                    op = self.admin_subopciones[self.subindice]
                    if op == "Cargar laberinto":
                        self.cargar_laberinto()
                    elif op == "Reiniciar salón":
                        self.reiniciar_salon_fama()
                    elif op == "Volver":
                        self.en_subadmin = False
        else:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    self.indice = (self.indice - 1) % len(self.opciones)
                elif e.key == pygame.K_DOWN:
                    self.indice = (self.indice + 1) % len(self.opciones)
                elif e.key == pygame.K_RETURN:
                    opcion = self.opciones[self.indice]
                    if opcion == "ADMINISTRACIÓN":
                        if self.autenticar_admin():
                            self.en_subadmin = True
                            self.subindice = 0
                    elif opcion == "JUEGO":
                        if self.verificar_laberintos_disponibles():
                            self.evento_mgr.publicar(EventoSeleccionMenu("JUEGO"))
                        else:
                            self.mostrar_mensaje_sin_laberintos()
                    elif opcion == "SALÓN DE LA FAMA":
                        self.evento_mgr.publicar(EventoSeleccionMenu("SALÓN_DE_LA_FAMA"))
                    elif opcion == "SALIR":
                        self.evento_mgr.publicar(EventoSeleccionMenu("SALIR"))

    def autenticar_admin(self):
        root = tk.Tk(); root.withdraw()
        try:
            password = simpledialog.askstring("Acceso Administrativo", "Ingrese la contraseña de administrador:", show='*')
            if password == self.admin_password:
                messagebox.showinfo("Acceso Concedido", "Bienvenido al panel administrativo"); return True
            elif password is not None:
                messagebox.showerror("Acceso Denegado", "Contraseña incorrecta")
            return False
        except Exception:
            return False
        finally:
            root.destroy()

    def verificar_laberintos_disponibles(self):
        try:
            ruta = "niveles.json" if os.path.exists("niveles.json") else "CODE_RUNNER/niveles.json"
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                return "niveles" in data and isinstance(data["niveles"], list) and len(data["niveles"]) > 0
        except Exception:
            return False

    def mostrar_mensaje_sin_laberintos(self):
        root = tk.Tk(); root.withdraw()
        messagebox.showwarning("Sin Laberintos", "No hay laberintos cargados.\n\nPara jugar, debe:\n1. Ir a ADMINISTRACIÓN\n2. Usar contraseña de administrador\n3. Cargar archivos de laberinto")
        root.destroy()

    def dibujar(self):
        self.vista.limpiar_pantalla((0, 0, 0))
        titulo_surf = self.fuente_titulo.render("Maze-Run", True, (255, 255, 255))
        x_titulo = (self.vista.ancho - titulo_surf.get_width()) // 2
        self.vista.pantalla.blit(titulo_surf, (x_titulo, 100))

        if self.en_subadmin:
            for i, opcion in enumerate(self.admin_subopciones):
                color = (255, 255, 0) if i == self.subindice else (200, 200, 200)
                surf = self.fuente_opcion.render(opcion, True, color)
                x_op = (self.vista.ancho - surf.get_width()) // 2
                y_op = 200 + i * 50
                self.vista.pantalla.blit(surf, (x_op, y_op))
        else:
            for i, opcion in enumerate(self.opciones):
                color = (255, 255, 0) if i == self.indice else (200, 200, 200)
                surf = self.fuente_opcion.render(opcion, True, color)
                x_op = (self.vista.ancho - surf.get_width()) // 2
                y_op = 200 + i * 50
                self.vista.pantalla.blit(surf, (x_op, y_op))

    def cargar_laberinto(self):
        root = tk.Tk(); root.withdraw()
        filetypes = [("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Seleccionar nuevo laberinto", filetypes=filetypes)
        if filename and os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if self.validar_estructura_laberinto(data):
                    with open("niveles.json", "w", encoding="utf-8") as fout:
                        json.dump(data, fout, indent=2, ensure_ascii=False)
                    messagebox.showinfo("Carga Exitosa", f"Se cargaron {len(data['niveles'])} laberinto(s) correctamente.\n\nYa puede jugar desde el menú principal.")
                else:
                    messagebox.showerror("Error de Validación", "El archivo no tiene el formato correcto.\n\nRequisitos:\n- Debe tener clave 'niveles'\n- Cada nivel debe tener: nombre, laberinto (matriz), entrada, salida\n- La matriz debe ser rectangular con valores válidos")
            except json.JSONDecodeError:
                messagebox.showerror("Error de Formato", "El archivo no es un JSON válido")
            except Exception as ex:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{ex}")
        root.destroy()

    def validar_estructura_laberinto(self, data):
        try:
            if not isinstance(data, dict) or "niveles" not in data:
                return False
            niveles = data["niveles"]
            if not isinstance(niveles, list) or len(niveles) == 0:
                return False
            for nivel in niveles:
                if not isinstance(nivel, dict):
                    return False
                for campo in ["nombre", "laberinto", "entrada", "salida"]:
                    if campo not in nivel:
                        return False
                lab = nivel["laberinto"]
                if not isinstance(lab, list) or len(lab) == 0:
                    return False
                w = len(lab[0])
                for fila in lab:
                    if not isinstance(fila, list) or len(fila) != w:
                        return False
                    for c in fila:
                        if not isinstance(c, int) or c not in [0,1,2,3]:
                            return False
                ent = nivel["entrada"]; sal = nivel["salida"]
                if (not isinstance(ent, list) or len(ent) != 2 or
                    not isinstance(sal, list) or len(sal) != 2):
                    return False
            return True
        except Exception:
            return False

    def reiniciar_salon_fama(self):
        try:
            with open("puntuaciones.json", "w", encoding="utf-8") as f:
                json.dump([], f)
            messagebox.showinfo("Reinicio Exitoso", "El salón de la fama ha sido vaciado correctamente.")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo vaciar el salón de la fama:\n{ex}")