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

    # Resto del archivo sin cambios...
