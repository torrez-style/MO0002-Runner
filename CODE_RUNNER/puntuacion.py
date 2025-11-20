import json
import os
from datetime import datetime
from typing import List, Dict


class GestorPuntuaciones:
    """Gestiona puntuaciones asociadas a usuarios"""

    def __init__(self, ruta_puntuaciones: str = "puntuaciones.json"):
        self.ruta_puntuaciones = os.path.join("CODE_RUNNER", ruta_puntuaciones)
        self._asegurar_archivo_existe()

    def _asegurar_archivo_existe(self):
        if not os.path.exists(self.ruta_puntuaciones):
            with open(self.ruta_puntuaciones, "w", encoding="utf-8") as f:
                json.dump({"puntuaciones": []}, f, ensure_ascii=False, indent=2)

    def guardar_puntuacion(self, nombre_usuario: str, puntos: int, nivel: int = 1):
        """Guarda una puntuación de un usuario"""
        puntuacion = {
            "nombre": nombre_usuario.upper(),
            "puntuacion": puntos,
            "nivel": nivel,
            "fecha": datetime.now().isoformat(),
        }

        puntuaciones = self._cargar_puntuaciones()
        puntuaciones.append(puntuacion)
        self._guardar_puntuaciones(puntuaciones)
        return puntuacion

    def obtener_top_puntuaciones(self, cantidad: int = 10) -> List[Dict]:
        """Obtiene las mejores puntuaciones"""
        puntuaciones = self._cargar_puntuaciones()
        # Agrupa por usuario y toma el máximo
        mejores_por_usuario = {}
        for p in puntuaciones:
            usuario = p["nombre"]
            if (
                usuario not in mejores_por_usuario
                or p["puntuacion"] > mejores_por_usuario[usuario]["puntuacion"]
            ):
                mejores_por_usuario[usuario] = p

        # Ordena por puntuación descendente
        ordenadas = sorted(
            mejores_por_usuario.values(), key=lambda x: x["puntuacion"], reverse=True
        )
        return ordenadas[:cantidad]

    def obtener_puntuaciones_usuario(self, nombre_usuario: str) -> List[Dict]:
        """Obtiene todas las puntuaciones de un usuario"""
        nombre_normalizado = nombre_usuario.upper()
        puntuaciones = self._cargar_puntuaciones()
        return [p for p in puntuaciones if p["nombre"] == nombre_normalizado]

    def obtener_puntuacion_maxima(self, nombre_usuario: str) -> int:
        """Obtiene la puntuación máxima de un usuario"""
        puntuaciones = self.obtener_puntuaciones_usuario(nombre_usuario)
        if not puntuaciones:
            return 0
        return max(p["puntuacion"] for p in puntuaciones)

    def _cargar_puntuaciones(self) -> List[Dict]:
        try:
            with open(self.ruta_puntuaciones, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("puntuaciones", [])
        except:
            return []

    def _guardar_puntuaciones(self, puntuaciones: List[Dict]):
        with open(self.ruta_puntuaciones, "w", encoding="utf-8") as f:
            json.dump({"puntuaciones": puntuaciones}, f, ensure_ascii=False, indent=2)
