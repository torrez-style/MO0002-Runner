import pygame
from evento import EventoSeleccionMenu
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import json

class MenuPrincipal:
    def __init__(self, vista, evento_mgr):
        self.vista = vista
        self.evento_mgr = evento_mgr
        self.opciones = ["JUEGO", "SALÓN_DE_LA_FAMA", "ADMINISTRACION", "SALIR"]
        self.admin_subopciones = ["Cargar laberinto", "Reiniciar salón", "Volver"]
        self.en_subadmin = False
        self.subindice = 0
        self.indice = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)

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
                    if opcion == "ADMINISTRACION":
                        self.en_subadmin = True
                        self.subindice = 0
                    else:
                        self.evento_mgr.publicar(EventoSeleccionMenu(opcion))

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
        root = tk.Tk()
        root.withdraw()
        filetypes = [("JSON files", "*.json"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Seleccionar nuevo laberinto", filetypes=filetypes)
        if filename and os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Pequeña validación básica
                if "niveles" in data and isinstance(data["niveles"], list) and data["niveles"]:
                    with open("niveles.json", "w", encoding="utf-8") as fout:
                        json.dump(data, fout, indent=2)
                    messagebox.showinfo("Carga exitosa", "El laberinto nuevo se cargó correctamente. Reinicia el juego para verlo.")
                else:
                    messagebox.showerror("Error de formato", "El archivo no es un laberinto válido. Debe tener la clave 'niveles'.")
            except Exception as ex:
                messagebox.showerror("Error", f"No se pudo cargar: {ex}")
        root.destroy()

    def reiniciar_salon_fama(self):
        try:
            with open("puntuaciones.json", "w", encoding="utf-8") as f:
                json.dump([], f)
            tk.messagebox.showinfo("Reinicio", "Salón de la fama vaciado.")
        except Exception as ex:
            tk.messagebox.showerror("Error", "No se pudo vaciar el salón: " + str(ex))
