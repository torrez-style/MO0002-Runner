import json
import os
from datetime import datetime
from typing import List, Dict, Optional


def _base_data_dir() -> str:
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))


class GestorPerfiles:
    """
    Gestiona perfiles de jugadores, puntuaciones y estadísticas.
    Mantiene coherencia entre perfiles.json y puntuaciones.json.
    """
    
    def __init__(self, ruta_perfiles="perfiles.json", ruta_puntuaciones="puntuaciones.json"):
        self.ruta_perfiles = ruta_perfiles
        self.ruta_puntuaciones = ruta_puntuaciones
        self.perfil_activo = None
    
    def _buscar_archivo(self, ruta: str) -> str:
        """Busca archivo primero en src/data, luego en raíz y CODE_RUNNER."""
        candidatos = [
            os.path.join(_base_data_dir(), os.path.basename(ruta)),
            ruta,
            os.path.join("CODE_RUNNER", ruta),
        ]
        return next((p for p in candidatos if os.path.exists(p)), candidatos[0])
    
    def _cargar_json(self, ruta: str, por_defecto=None) -> List[Dict]:
        """Carga archivo JSON de forma segura."""
        ruta_real = self._buscar_archivo(ruta)
        try:
            with open(ruta_real, 'r', encoding='utf-8') as f:
                texto = f.read().strip()
                return json.loads(texto) if texto else (por_defecto or [])
        except (FileNotFoundError, json.JSONDecodeError):
            return por_defecto or []
    
    def _guardar_json(self, ruta: str, datos: List[Dict]) -> bool:
        """Guarda archivo JSON de forma segura en src/data."""
        try:
            os.makedirs(_base_data_dir(), exist_ok=True)
            ruta_destino = os.path.join(_base_data_dir(), os.path.basename(ruta))
            with open(ruta_destino, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error guardando {ruta}: {e}")
            return False
    
    def cargar_perfiles(self) -> List[Dict]:
        """Carga lista de perfiles disponibles."""
        return self._cargar_json(self.ruta_perfiles, [])
    
    def crear_perfil(self, nombre: str) -> Optional[Dict]:
        """Crea un nuevo perfil de jugador."""
        if not nombre or not nombre.strip():
            return None
        
        perfiles = self.cargar_perfiles()
        
        # Verificar que no existe
        if any(p.get('nombre', '').lower() == nombre.lower() for p in perfiles):
            return None
        
        # Generar ID
        nuevo_id = max((p.get('id', 0) for p in perfiles), default=0) + 1
        
        nuevo_perfil = {
            'id': nuevo_id,
            'nombre': nombre.strip(),
            'fecha_creacion': datetime.now().strftime('%Y-%m-%d'),
            'partidas_jugadas': 0,
            'mejor_puntuacion': 0
        }
        
        perfiles.append(nuevo_perfil)
        
        if self._guardar_json(self.ruta_perfiles, perfiles):
            return nuevo_perfil
        return None
    
    def seleccionar_perfil(self, perfil_id: int) -> Optional[Dict]:
        """Selecciona un perfil como activo."""
        perfiles = self.cargar_perfiles()
        perfil = next((p for p in perfiles if p.get('id') == perfil_id), None)
        if perfil:
            self.perfil_activo = perfil
        return perfil
    
    def obtener_perfil_activo(self) -> Optional[Dict]:
        """Devuelve el perfil actualmente seleccionado."""
        return self.perfil_activo
    
    def registrar_partida(self, puntuacion: int) -> bool:
        """Registra una partida completada para el perfil activo."""
        if not self.perfil_activo:
            return False
        
        # Actualizar estadísticas del perfil
        perfiles = self.cargar_perfiles()
        perfil_id = self.perfil_activo['id']
        
        for perfil in perfiles:
            if perfil.get('id') == perfil_id:
                perfil['partidas_jugadas'] = perfil.get('partidas_jugadas', 0) + 1
                perfil['mejor_puntuacion'] = max(perfil.get('mejor_puntuacion', 0), puntuacion)
                break
        
        # Registrar puntuación individual
        puntuaciones = self._cargar_json(self.ruta_puntuaciones, [])
        puntuaciones.append({
            'perfil_id': perfil_id,
            'nombre': self.perfil_activo['nombre'],
            'puntuacion': puntuacion,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
        # Guardar ambos archivos
        perfil_ok = self._guardar_json(self.ruta_perfiles, perfiles)
        puntuacion_ok = self._guardar_json(self.ruta_puntuaciones, puntuaciones)
        
        return perfil_ok and puntuacion_ok
    
    def obtener_ranking_global(self, limite: int = 10) -> List[Dict]:
        """Obtiene ranking global de mejores puntuaciones."""
        puntuaciones = self._cargar_json(self.ruta_puntuaciones, [])
        puntuaciones_ordenadas = sorted(
            puntuaciones, 
            key=lambda x: x.get('puntuacion', 0), 
            reverse=True
        )
        return puntuaciones_ordenadas[:limite]
    
    def obtener_ranking_por_perfil(self, limite: int = 10) -> List[Dict]:
        """Obtiene ranking por mejor puntuación de cada perfil."""
        perfiles = self.cargar_perfiles()
        perfiles_con_puntuacion = [
            p for p in perfiles 
            if p.get('mejor_puntuacion', 0) > 0
        ]
        perfiles_ordenados = sorted(
            perfiles_con_puntuacion,
            key=lambda x: x.get('mejor_puntuacion', 0),
            reverse=True
        )
        return perfiles_ordenados[:limite]
    
    def eliminar_perfil(self, perfil_id: int) -> bool:
        """Elimina un perfil y sus puntuaciones asociadas."""
        perfiles = self.cargar_perfiles()
        perfiles_filtrados = [p for p in perfiles if p.get('id') != perfil_id]
        
        if len(perfiles_filtrados) == len(perfiles):
            return False  # No existía el perfil
        
        puntuaciones = self._cargar_json(self.ruta_puntuaciones, [])
        puntuaciones_filtradas = [p for p in puntuaciones if p.get('perfil_id') != perfil_id]
        
        # Si era el perfil activo, desactivarlo
        if self.perfil_activo and self.perfil_activo.get('id') == perfil_id:
            self.perfil_activo = None
        
        perfil_ok = self._guardar_json(self.ruta_perfiles, perfiles_filtrados)
        puntuacion_ok = self._guardar_json(self.ruta_puntuaciones, puntuaciones_filtradas)
        
        return perfil_ok and puntuacion_ok
