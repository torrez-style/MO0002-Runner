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
        self.opciones = ["JUEGO", "SALÓN_DE_LA_FAMA", "ADMINISTRACION", "SALIR"]
        self.admin_subopciones = ["Cargar laberinto", "Reiniciar salón", "Volver"]
        self.en_subadmin = False
        self.subindice = 0
        self.indice = 0
        self.fuente_titulo = pygame.font.SysFont(None, 48)
        self.fuente_opcion = pygame.font.SysFont(None, 36)
        # Contraseña para acceso administrativo según HU-015
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
                    if opcion == "ADMINISTRACION":
                        # Requerir autenticación según HU-015
                        if self.autenticar_admin():
                            self.en_subadmin = True
                            self.subindice = 0
                    elif opcion == "JUEGO":
                        # Verificar que existan laberintos cargados
                        if self.verificar_laberintos_disponibles():
                            self.evento_mgr.publicar(EventoSeleccionMenu(opcion))
                        else:
                            self.mostrar_mensaje_sin_laberintos()
                    else:
                        self.evento_mgr.publicar(EventoSeleccionMenu(opcion))

    def autenticar_admin(self):
        """Solicita contraseña para acceso administrativo según HU-015"""
        root = tk.Tk()
        root.withdraw()
        try:
            password = simpledialog.askstring(
                "Acceso Administrativo", 
                "Ingrese la contraseña de administrador:", 
                show='*'
            )
            if password == self.admin_password:
                messagebox.showinfo("Acceso Concedido", "Bienvenido al panel administrativo")
                return True
            elif password is not None:  # Si no canceló
                messagebox.showerror("Acceso Denegado", "Contraseña incorrecta")
            return False
        except Exception:
            return False
        finally:
            root.destroy()

    def verificar_laberintos_disponibles(self):
        """Verifica si hay laberintos cargados para jugar - Fix de ruta"""
        try:
            # Intentar primero la ruta relativa (cuando se ejecuta desde CODE_RUNNER/)
            ruta_niveles = "niveles.json"
            if not os.path.exists(ruta_niveles):
                # Fallback a ruta completa
                ruta_niveles = "CODE_RUNNER/niveles.json"
                
            with open(ruta_niveles, "r", encoding="utf-8") as f:
                data = json.load(f)
                hay_niveles = "niveles" in data and isinstance(data["niveles"], list) and len(data["niveles"]) > 0
                print(f"DEBUG: Verificando laberintos en {ruta_niveles}: {hay_niveles}")
                if hay_niveles:
                    print(f"DEBUG: Encontrados {len(data['niveles'])} niveles")
                return hay_niveles
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"DEBUG: Error verificando laberintos: {e}")
            return False

    def mostrar_mensaje_sin_laberintos(self):
        """Informa al usuario que debe cargar laberintos desde administración"""
        root = tk.Tk()
        root.withdraw()
        messagebox.showwarning(
            "Sin Laberintos", 
            "No hay laberintos cargados.\n\nPara jugar, debe:\n1. Ir a ADMINISTRACIÓN\n2. Usar contraseña de administrador\n3. Cargar archivos de laberinto\n\nContacte al administrador si no tiene acceso."
        )
        root.destroy()

    def dibujar(self):
        self.vista.limpiar_pantalla((0, 0, 0))
        titulo_surf = self.fuente_titulo.render("Maze-Run", True, (255, 255, 255))
        x_titulo = (self.vista.ancho - titulo_surf.get_width()) // 2
        self.vista.pantalla.blit(titulo_surf, (x_titulo, 100))
        
        if self.en_subadmin:
            # Mostrar opciones administrativas
            for i, opcion in enumerate(self.admin_subopciones):
                color = (255, 255, 0) if i == self.subindice else (200, 200, 200)
                surf = self.fuente_opcion.render(opcion, True, color)
                x_op = (self.vista.ancho - surf.get_width()) // 2
                y_op = 200 + i * 50
                self.vista.pantalla.blit(surf, (x_op, y_op))
        else:
            # Mostrar menú principal con indicador de estado
            laberintos_disponibles = self.verificar_laberintos_disponibles()
            for i, opcion in enumerate(self.opciones):
                color = (255, 255, 0) if i == self.indice else (200, 200, 200)
                
                # Agregar indicador para JUEGO
                texto_opcion = opcion
                if opcion == "JUEGO":
                    if laberintos_disponibles:
                        texto_opcion += " (✓ Listo)"  # Checkmark
                        color = (100, 255, 100) if i != self.indice else (150, 255, 150)
                    else:
                        texto_opcion += " (Sin laberintos)"
                        color = (150, 150, 150) if i != self.indice else (255, 200, 100)
                
                surf = self.fuente_opcion.render(texto_opcion, True, color)
                x_op = (self.vista.ancho - surf.get_width()) // 2
                y_op = 200 + i * 50
                self.vista.pantalla.blit(surf, (x_op, y_op))

    def cargar_laberinto(self):
        """Cargar laberinto con validación mejorada según HU-017"""
        root = tk.Tk()
        root.withdraw()
        filetypes = [("JSON files", "*.json"), ("Text files", "*.txt"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(
            title="Seleccionar nuevo laberinto", 
            filetypes=filetypes
        )
        
        if filename and os.path.exists(filename):
            try:
                with open(filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Validación completa según HU-017
                if self.validar_estructura_laberinto(data):
                    # Guardar en el archivo de niveles - usar ruta relativa
                    ruta_destino = "niveles.json"
                    with open(ruta_destino, "w", encoding="utf-8") as fout:
                        json.dump(data, fout, indent=2, ensure_ascii=False)
                    
                    print(f"DEBUG: Laberintos guardados en {ruta_destino}")
                    messagebox.showinfo(
                        "Carga Exitosa", 
                        f"Se cargaron {len(data['niveles'])} laberinto(s) correctamente.\n\nYa puede jugar desde el menú principal."
                    )
                else:
                    messagebox.showerror(
                        "Error de Validación", 
                        "El archivo no tiene el formato correcto.\n\nRequisitos:\n- Debe tener clave 'niveles'\n- Cada nivel debe tener: nombre, laberinto (matriz), entrada, salida\n- La matriz debe ser rectangular con valores válidos"
                    )
            except json.JSONDecodeError:
                messagebox.showerror("Error de Formato", "El archivo no es un JSON válido")
            except Exception as ex:
                messagebox.showerror("Error", f"No se pudo cargar el archivo:\n{ex}")
        
        root.destroy()

    def validar_estructura_laberinto(self, data):
        """Validación completa de estructura de laberinto según HU-017"""
        try:
            # Verificar estructura principal
            if not isinstance(data, dict) or "niveles" not in data:
                return False
            
            niveles = data["niveles"]
            if not isinstance(niveles, list) or len(niveles) == 0:
                return False
            
            # Validar cada nivel
            for nivel in niveles:
                if not isinstance(nivel, dict):
                    return False
                
                # Campos requeridos
                campos_requeridos = ["nombre", "laberinto", "entrada", "salida"]
                for campo in campos_requeridos:
                    if campo not in nivel:
                        return False
                
                # Validar matriz del laberinto
                laberinto = nivel["laberinto"]
                if not isinstance(laberinto, list) or len(laberinto) == 0:
                    return False
                
                # Verificar que sea rectangular
                ancho = len(laberinto[0]) if laberinto else 0
                for fila in laberinto:
                    if not isinstance(fila, list) or len(fila) != ancho:
                        return False
                    # Verificar valores válidos (0=camino, 1=pared, 2=entrada, 3=salida)
                    for celda in fila:
                        if not isinstance(celda, int) or celda not in [0, 1, 2, 3]:
                            return False
                
                # Validar coordenadas de entrada y salida
                entrada = nivel["entrada"]
                salida = nivel["salida"]
                if (not isinstance(entrada, list) or len(entrada) != 2 or
                    not isinstance(salida, list) or len(salida) != 2):
                    return False
            
            return True
        except Exception:
            return False

    def reiniciar_salon_fama(self):
        """Reinicia el salón de la fama vaciando puntuaciones"""
        try:
            ruta_puntuaciones = "puntuaciones.json"
            with open(ruta_puntuaciones, "w", encoding="utf-8") as f:
                json.dump([], f)
            messagebox.showinfo("Reinicio Exitoso", "El salón de la fama ha sido vaciado correctamente.")
        except Exception as ex:
            messagebox.showerror("Error", f"No se pudo vaciar el salón de la fama:\n{ex}")