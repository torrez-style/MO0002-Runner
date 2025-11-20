import json
import os
from datetime import datetime


class SalondelaFama:
    """Gestiona el salón de la fama y rankings del juego."""

    def __init__(
        self, archivo_puntuaciones="puntuaciones.json", archivo_perfiles="perfiles.json"
    ):
        self.archivo_puntuaciones = archivo_puntuaciones
        self.archivo_perfiles = archivo_perfiles
        self._inicializar_archivos()

    def _inicializar_archivos(self):
        """Crea los archivos JSON si no existen."""
        if not os.path.exists(self.archivo_puntuaciones):
            with open(self.archivo_puntuaciones, "w", encoding="utf-8") as f:
                json.dump({"puntuaciones": []}, f, ensure_ascii=False, indent=4)

        if not os.path.exists(self.archivo_perfiles):
            with open(self.archivo_perfiles, "w", encoding="utf-8") as f:
                json.dump({"usuarios": []}, f, ensure_ascii=False, indent=4)

    def _cargar_puntuaciones(self):
        """Carga puntuaciones desde JSON."""
        try:
            with open(self.archivo_puntuaciones, "r", encoding="utf-8") as f:
                datos = json.load(f)
                return datos.get("puntuaciones", [])
        except:
            return []

    def _guardar_puntuaciones(self, puntuaciones):
        """Guarda puntuaciones en JSON."""
        with open(self.archivo_puntuaciones, "w", encoding="utf-8") as f:
            json.dump({"puntuaciones": puntuaciones}, f, ensure_ascii=False, indent=4)

    def registrar_puntuacion(self, usuario, puntos, nivel):
        """Registra nueva puntuación."""
        usuario = usuario.upper()
        puntuaciones = self._cargar_puntuaciones()

        nueva_puntuacion = {
            "usuario": usuario,
            "puntos": puntos,
            "nivel": nivel,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        puntuaciones.append(nueva_puntuacion)
        self._guardar_puntuaciones(puntuaciones)

    def obtener_ranking_general(self, limite=10):
        """Obtiene top 10 de todas las puntuaciones."""
        puntuaciones = self._cargar_puntuaciones()
        ordenadas = sorted(puntuaciones, key=lambda x: x["puntos"], reverse=True)
        return ordenadas[:limite]

    def obtener_mejor_puntuacion_usuario(self, usuario):
        """Obtiene mejor puntuación de un usuario."""
        usuario = usuario.upper()
        puntuaciones = self._cargar_puntuaciones()
        puntuaciones_usuario = [p for p in puntuaciones if p["usuario"] == usuario]

        if not puntuaciones_usuario:
            return None

        return sorted(puntuaciones_usuario, key=lambda x: x["puntos"], reverse=True)[0]

    def obtener_posicion_usuario(self, usuario):
        """Obtiene posición en ranking."""
        usuario = usuario.upper()
        ranking = self.obtener_ranking_general(limite=100)

        for indice, puntuacion in enumerate(ranking, 1):
            if puntuacion["usuario"] == usuario:
                return indice

        return -1

    def obtener_estadisticas_usuario(self, usuario):
        """Obtiene estadísticas completas del usuario."""
        usuario = usuario.upper()
        puntuaciones = self._cargar_puntuaciones()
        puntuaciones_usuario = [p for p in puntuaciones if p["usuario"] == usuario]

        if not puntuaciones_usuario:
            return None

        puntos_totales = sum(p["puntos"] for p in puntuaciones_usuario)
        mejor = max([p["puntos"] for p in puntuaciones_usuario])
        promedio = puntos_totales / len(puntuaciones_usuario)

        return {
            "usuario": usuario,
            "total_partidas": len(puntuaciones_usuario),
            "mejor_puntuacion": mejor,
            "promedio": round(promedio, 2),
            "puntos_totales": puntos_totales,
            "posicion": self.obtener_posicion_usuario(usuario),
        }
