"""
Configuración centralizada del juego Maze Runner
MO0002 - Programación I - Universidad de Costa Rica
"""

from dataclasses import dataclass
from typing import Tuple, Dict
import os


@dataclass
class GameSettings:
    """Configuración principal del juego"""
    
    # === CONFIGURACIÓN DE PANTALLA ===
    SCREEN_WIDTH: int = 900
    SCREEN_HEIGHT: int = 700
    FPS: int = 60
    WINDOW_TITLE: str = "Maze Runner - MO0002"
    
    # === CONFIGURACIÓN DE JUEGO ===
    PLAYER_LIVES: int = 3
    POINTS_PER_MOVE: int = 1
    POINTS_PER_ITEM: int = 10
    ENEMY_SPEED_BASE: int = 14
    ENEMY_SPEED_MULTIPLIER: float = 1.1
    POWERUP_DURATION: int = 300  # frames
    PLAYER_STEP_DELAY: int = 7
    
    # === CONFIGURACIÓN DE ARCHIVOS ===
    LEVELS_FILE: str = "assets/config/levels.json"
    SCORES_FILE: str = "assets/data/scores.json"
    PROFILES_FILE: str = "assets/data/profiles.json"
    CONFIG_FILE: str = "config/config.json"
    
    # === CONFIGURACIÓN DE AUDIO ===
    ENABLE_SOUND: bool = True
    MASTER_VOLUME: float = 0.7
    SFX_VOLUME: float = 0.8
    
    # === CONFIGURACIÓN DE ADMINISTRACIÓN ===
    ADMIN_PASSWORD: str = "admin2025"
    
    # === CONFIGURACIÓN DE LABERINTO ===
    CELL_SIZE: int = 32
    MAZE_PADDING: int = 20
    
    # === COLORES DEFAULT ===
    COLORS: Dict[str, Tuple[int, int, int]] = None
    
    def __post_init__(self):
        """Inicializa colores después de la creación"""
        if self.COLORS is None:
            self.COLORS = {
                'background': (0, 0, 0),
                'wall': (80, 80, 80),
                'floor': (220, 230, 245),
                'player': (50, 150, 255),
                'enemy': (220, 50, 50),
                'star': (255, 255, 0),
                'powerup': (255, 0, 255),
                'text': (255, 255, 255),
                'menu_selected': (255, 255, 0),
                'menu_normal': (200, 200, 200)
            }
    
    @classmethod
    def load_from_file(cls, config_path: str = None):
        """Carga configuración desde archivo JSON"""
        # Implementación futura para cargar desde config.json
        return cls()
    
    def save_to_file(self, config_path: str = None):
        """Guarda configuración actual a archivo JSON"""
        # Implementación futura para guardar en config.json
        pass


# Instancia global de configuración
settings = GameSettings()


class Paths:
    """Rutas de archivos y directorios del proyecto"""
    
    @staticmethod
    def get_asset_path(filename: str) -> str:
        """Obtiene ruta completa de un asset"""
        return os.path.join("assets", filename)
    
    @staticmethod
    def get_sound_path(filename: str) -> str:
        """Obtiene ruta completa de un archivo de sonido"""
        return os.path.join("assets", "sounds", filename)
    
    @staticmethod
    def get_config_path(filename: str) -> str:
        """Obtiene ruta completa de un archivo de configuración"""
        return os.path.join("assets", "config", filename)
    
    @staticmethod
    def get_data_path(filename: str) -> str:
        """Obtiene ruta completa de un archivo de datos"""
        return os.path.join("assets", "data", filename)
