import json
import os
from datetime import datetime

class SalonDeLaFama:
    def __init__(self, archivo="puntuaciones.json"):
        self.archivo = archivo
        self.puntuaciones = self._cargar_puntuaciones()

    def _cargar_puntuaciones(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r") as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _guardar_puntuaciones(self):
        with open(self.archivo, "w") as f:
            json.dump(self.puntuaciones, f, indent=4)

    # ACEPTA NIVEL Y NOMBRE_LABERINTO
    def registrar_puntuacion(self, usuario, puntuacion, nivel, nombre_laberinto, tiempo=None):
        if usuario not in self.puntuaciones:
            self.puntuaciones[usuario] = []
        data = {
            "puntuacion": puntuacion,
            "nivel": nivel,
            "laberinto": nombre_laberinto,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        if tiempo is not None:
            data["tiempo"] = tiempo
        self.puntuaciones[usuario].append(data)
        self._guardar_puntuaciones()

    def obtener_ranking_global(self):
        ranking = []
        for usuario, partidas in self.puntuaciones.items():
            if partidas:
                mejor_puntuacion = max(p["puntuacion"] for p in partidas)
                ranking.append((usuario, mejor_puntuacion))

        ranking.sort(key=lambda x: x[1], reverse=True)

        if not ranking:
            return "No hay puntuaciones registradas."

        resultado = "=== RANKING GLOBAL ===\n"
        for i, (usuario, puntuacion) in enumerate(ranking, 1):
            resultado += f"{i}. {usuario}: {puntuacion} puntos\n"

        return resultado

    def eliminar_puntuaciones_usuario(self, usuario):
        if usuario in self.puntuaciones:
            del self.puntuaciones[usuario]
            self._guardar_puntuaciones()
            return True
        return False
