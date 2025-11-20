import json
import os
from typing import Optional, List, Dict


class GestorUsuarios:
    """Gestiona usuarios con nombres normalizados a mayúsculas"""

    def __init__(self, ruta_perfiles: str = "perfiles.json"):
        self.ruta_perfiles = os.path.join("CODE_RUNNER", ruta_perfiles)
        self._asegurar_archivo_existe()

    def _asegurar_archivo_existe(self):
        if not os.path.exists(self.ruta_perfiles):
            with open(self.ruta_perfiles, "w", encoding="utf-8") as f:
                json.dump({"usuarios": []}, f, ensure_ascii=False, indent=2)

    def normalizar_nombre(self, nombre: str) -> str:
        """Convierte nombre a mayúsculas y elimina espacios extra"""
        return nombre.strip().upper()

    def usuario_existe(self, nombre: str) -> bool:
        """Verifica si un usuario ya existe"""
        nombre_normalizado = self.normalizar_nombre(nombre)
        usuarios = self._cargar_usuarios()
        return any(u["nombre"] == nombre_normalizado for u in usuarios)

    def crear_usuario(self, nombre: str) -> Dict:
        """Crea un nuevo usuario si no existe"""
        if not nombre or not nombre.strip():
            raise ValueError("El nombre de usuario no puede estar vacío")

        nombre_normalizado = self.normalizar_nombre(nombre)

        if self.usuario_existe(nombre_normalizado):
            raise ValueError(f"El usuario '{nombre_normalizado}' ya existe")

        usuario = {
            "nombre": nombre_normalizado,
            "partidas_jugadas": 0,
            "puntuacion_maxima": 0,
            "fecha_creacion": str(__import__("datetime").datetime.now()),
        }

        usuarios = self._cargar_usuarios()
        usuarios.append(usuario)
        self._guardar_usuarios(usuarios)
        return usuario

    def obtener_usuario(self, nombre: str) -> Optional[Dict]:
        """Obtiene info de un usuario"""
        nombre_normalizado = self.normalizar_nombre(nombre)
        usuarios = self._cargar_usuarios()
        return next((u for u in usuarios if u["nombre"] == nombre_normalizado), None)

    def _cargar_usuarios(self) -> List[Dict]:
        try:
            with open(self.ruta_perfiles, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("usuarios", [])
        except:
            return []

    def _guardar_usuarios(self, usuarios: List[Dict]):
        with open(self.ruta_perfiles, "w", encoding="utf-8") as f:
            json.dump({"usuarios": usuarios}, f, ensure_ascii=False, indent=2)
