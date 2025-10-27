"""
Módulo Core - Motor principal del juego
Contiene el motor del juego y gestor de estados
"""

from .game_engine import GameEngine
from .game_state import GameStateManager, GameState, GameData

__all__ = ['GameEngine', 'GameStateManager', 'GameState', 'GameData']
