import json
import os
from datetime import datetime


class SalonDeLaFama:
    """Gestiona el ranking de puntuaciones por usuario."""
    
    def __init__(self, archivo_puntuaciones="CODE_RUNNER/puntuaciones.json"):
        self.archivo = archivo_puntuaciones
        self.puntuaciones = self._cargar_puntuaciones()
    
    def _cargar_puntuaciones(self):
        """Carga las puntuaciones desde el archivo JSON."""
        try:
            if os.path.exists(self.archivo):
                with open(self.archivo, "r", encoding="utf-8") as f:
                    datos = json.load(f)
                    return datos if isinstance(datos, dict) else {}
            return {}
        except Exception:
            return {}
    
    def _guardar_puntuaciones(self):
        """Guarda las puntuaciones en el archivo JSON."""
        try:
            os.makedirs(os.path.dirname(self.archivo) or ".", exist_ok=True)
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(self.puntuaciones, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error al guardar puntuaciones: {e}")
    
    def registrar_puntuacion(self, usuario, puntuacion, nivel=1, nombre_laberinto="Desconocido"):
        """Registra una nueva puntuación para un usuario."""
        usuario = usuario.strip().upper()
        
        # Validar entrada
        if not usuario:
            return False
        if not isinstance(puntuacion, (int, float)) or puntuacion < 0:
            return False
        
        # Crear entrada de usuario si no existe
        if usuario not in self.puntuaciones:
            self.puntuaciones[usuario] = []
        
        # Agregar nueva puntuación
        registro = {
            "puntuacion": int(puntuacion),
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "nivel": int(nivel),
            "laberinto": nombre_laberinto
        }
        
        self.puntuaciones[usuario].append(registro)
        self._guardar_puntuaciones()
        return True
    
    def obtener_mejores_puntuaciones(self, usuario, limite=10):
        """Obtiene las mejores puntuaciones de un usuario."""
        usuario = usuario.strip().upper()
        
        if usuario not in self.puntuaciones:
            return []
        
        # Ordenar de mayor a menor puntuación
        puntuaciones_ordenadas = sorted(
            self.puntuaciones[usuario],
            key=lambda x: x["puntuacion"],
            reverse=True
        )
        
        return puntuaciones_ordenadas[:limite]
    
    def obtener_ranking_global(self, limite=10):
        """Obtiene el ranking global (mejores puntuaciones de todos los usuarios)."""
        ranking = []
        
        for usuario, puntuaciones in self.puntuaciones.items():
            if puntuaciones:
                mejor = max(puntuaciones, key=lambda x: x["puntuacion"])
                ranking.append({
                    "usuario": usuario,
                    "puntuacion": mejor["puntuacion"],
                    "fecha": mejor["fecha"],
                    "nivel": mejor["nivel"],
                    "laberinto": mejor.get("laberinto", "Desconocido")
                })
        
        # Ordenar de mayor a menor
        ranking_ordenado = sorted(
            ranking,
            key=lambda x: x["puntuacion"],
            reverse=True
        )
        
        return ranking_ordenado[:limite]
    
    def obtener_estadisticas_usuario(self, usuario):
        """Obtiene estadísticas de un usuario."""
        usuario = usuario.strip().upper()
        
        if usuario not in self.puntuaciones or not self.puntuaciones[usuario]:
            return None
        
        puntuaciones_list = [p["puntuacion"] for p in self.puntuaciones[usuario]]
        
        return {
            "usuario": usuario,
            "total_partidas": len(puntuaciones_list),
            "mejor_puntuacion": max(puntuaciones_list),
            "peor_puntuacion": min(puntuaciones_list),
            "promedio": sum(puntuaciones_list) / len(puntuaciones_list),
            "ultimas_partidas": self.puntuaciones[usuario][-5:]  # Últimas 5
        }
    
    def eliminar_usuario(self, usuario):
        """Elimina todas las puntuaciones de un usuario."""
        usuario = usuario.strip().upper()
        
        if usuario in self.puntuaciones:
            del self.puntuaciones[usuario]
            self._guardar_puntuaciones()
            return True
        return False
    
    def reiniciar_salon_completo(self):
        """Reinicia el salón de la fama completamente."""
        self.puntuaciones = {}
        self._guardar_puntuaciones()
