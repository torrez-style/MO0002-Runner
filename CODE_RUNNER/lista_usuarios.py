import json
import os

class ListaUsuarios:
    def __init__(self, archivo="usuarios.json"):
        self.archivo = archivo
        self.usuarios = self._cargar_usuarios()
    
    def _cargar_usuarios(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _guardar_usuarios(self):
        with open(self.archivo, 'w') as f:
            json.dump(self.usuarios, f, indent=4)
    
    def crear_usuario(self, nombre):
        nombre = nombre.upper()
        if nombre not in self.usuarios:
            self.usuarios.append(nombre)
            self._guardar_usuarios()
            return True
        return False
    
    def eliminar_usuario(self, nombre):
        nombre = nombre.upper()
        if nombre in self.usuarios:
            self.usuarios.remove(nombre)
            self._guardar_usuarios()
            return True
        return False
    
    def listar_todos(self):
        if not self.usuarios:
            print("No hay usuarios registrados.")
        else:
            print("\n=== USUARIOS REGISTRADOS ===")
            for i, usuario in enumerate(self.usuarios, 1):
                print(f"{i}. {usuario}")
    
    def usuario_existe(self, nombre):
        return nombre.upper() in self.usuarios
