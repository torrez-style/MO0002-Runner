"""
Sistema de gestión de estados del juego Maze Runner
Implementa el patrón State Machine para manejar diferentes estados del juego

MO0002 - Programación I - Universidad de Costa Rica
"""

from enum import Enum, auto
from typing import Dict, Callable, Optional
from dataclasses import dataclass
from datetime import datetime


class GameState(Enum):
    """Estados posibles del juego"""
    MENU = auto()
    PLAYING = auto()
    PAUSED = auto()
    GAME_OVER = auto()
    HALL_OF_FAME = auto()
    ADMINISTRATION = auto()
    LOADING = auto()


@dataclass
class GameData:
    """Datos del estado actual del juego"""
    player_name: str = ""
    current_level: int = 0
    score: int = 0
    lives: int = 3
    stars_collected: int = 0
    total_stars: int = 0
    game_started_at: Optional[datetime] = None
    game_duration: float = 0.0
    powerup_active: Optional[str] = None
    powerup_timer: int = 0


class GameStateManager:
    """
    Administrador de estados del juego
    Implementa máquina de estados finita
    """
    
    def __init__(self, initial_state: GameState = GameState.MENU):
        self.current_state = initial_state
        self.previous_state = None
        self.state_stack = [initial_state]  # Para manejar estados temporales
        self.game_data = GameData()
        
        # Transiciones válidas entre estados
        self.valid_transitions: Dict[GameState, list[GameState]] = {
            GameState.MENU: [
                GameState.PLAYING,
                GameState.HALL_OF_FAME,
                GameState.ADMINISTRATION,
                GameState.LOADING
            ],
            GameState.PLAYING: [
                GameState.PAUSED,
                GameState.GAME_OVER,
                GameState.MENU,
                GameState.LOADING
            ],
            GameState.PAUSED: [
                GameState.PLAYING,
                GameState.MENU
            ],
            GameState.GAME_OVER: [
                GameState.PLAYING,
                GameState.MENU,
                GameState.HALL_OF_FAME
            ],
            GameState.HALL_OF_FAME: [
                GameState.MENU
            ],
            GameState.ADMINISTRATION: [
                GameState.MENU,
                GameState.LOADING
            ],
            GameState.LOADING: [
                GameState.MENU,
                GameState.PLAYING
            ]
        }
        
        # Callbacks para entrada y salida de estados
        self.on_enter_callbacks: Dict[GameState, list[Callable]] = {}
        self.on_exit_callbacks: Dict[GameState, list[Callable]] = {}
        
        # Inicializar callbacks
        for state in GameState:
            self.on_enter_callbacks[state] = []
            self.on_exit_callbacks[state] = []
    
    def change_state(self, new_state: GameState, force: bool = False) -> bool:
        """
        Cambia al nuevo estado si la transición es válida
        
        Args:
            new_state: El estado al que se quiere cambiar
            force: Si es True, ignora las validaciones de transición
        
        Returns:
            True si el cambio fue exitoso, False si no
        """
        if not force and not self.is_valid_transition(new_state):
            print(f"⚠️  Transición inválida: {self.current_state.name} -> {new_state.name}")
            return False
        
        print(f"🔄 Cambiando estado: {self.current_state.name} -> {new_state.name}")
        
        # Ejecutar callbacks de salida del estado actual
        for callback in self.on_exit_callbacks[self.current_state]:
            callback()
        
        # Cambiar estado
        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_stack.append(new_state)
        
        # Ejecutar callbacks de entrada del nuevo estado
        for callback in self.on_enter_callbacks[self.current_state]:
            callback()
        
        return True
    
    def is_valid_transition(self, new_state: GameState) -> bool:
        """Verifica si la transición es válida"""
        return new_state in self.valid_transitions.get(self.current_state, [])
    
    def push_state(self, new_state: GameState) -> bool:
        """
        Empuja un estado temporal (para menús de pausa, etc.)
        El estado anterior se mantiene en la pila
        """
        if self.change_state(new_state):
            return True
        return False
    
    def pop_state(self) -> bool:
        """
        Regresa al estado anterior en la pila
        """
        if len(self.state_stack) > 1:
            self.state_stack.pop()  # Remover estado actual
            previous_state = self.state_stack[-1]  # Obtener el anterior
            return self.change_state(previous_state, force=True)
        return False
    
    def register_enter_callback(self, state: GameState, callback: Callable) -> None:
        """Registra un callback para cuando se entra a un estado"""
        self.on_enter_callbacks[state].append(callback)
    
    def register_exit_callback(self, state: GameState, callback: Callable) -> None:
        """Registra un callback para cuando se sale de un estado"""
        self.on_exit_callbacks[state].append(callback)
    
    def reset_game_data(self) -> None:
        """Reinicia los datos del juego"""
        self.game_data = GameData()
        self.game_data.game_started_at = datetime.now()
        print("🔄 Datos del juego reiniciados")
    
    def start_new_game(self, player_name: str = "Jugador") -> None:
        """Inicia un nuevo juego"""
        self.reset_game_data()
        self.game_data.player_name = player_name
        self.game_data.lives = 3
        self.game_data.score = 0
        self.change_state(GameState.PLAYING)
        print(f"🎮 Nuevo juego iniciado para: {player_name}")
    
    def end_game(self, final_score: int) -> None:
        """Termina el juego actual"""
        if self.game_data.game_started_at:
            duration = datetime.now() - self.game_data.game_started_at
            self.game_data.game_duration = duration.total_seconds()
        
        self.game_data.score = final_score
        self.change_state(GameState.GAME_OVER)
        print(f"🏁 Juego terminado - Puntuación: {final_score}")
    
    def pause_game(self) -> bool:
        """Pausa el juego si está jugando"""
        if self.current_state == GameState.PLAYING:
            return self.change_state(GameState.PAUSED)
        return False
    
    def resume_game(self) -> bool:
        """Reanuda el juego si está en pausa"""
        if self.current_state == GameState.PAUSED:
            return self.change_state(GameState.PLAYING)
        return False
    
    def get_state_info(self) -> dict:
        """Obtiene información del estado actual"""
        return {
            'current_state': self.current_state.name,
            'previous_state': self.previous_state.name if self.previous_state else None,
            'state_stack_size': len(self.state_stack),
            'game_data': {
                'player_name': self.game_data.player_name,
                'level': self.game_data.current_level,
                'score': self.game_data.score,
                'lives': self.game_data.lives,
                'stars_collected': self.game_data.stars_collected,
                'total_stars': self.game_data.total_stars,
                'game_duration': self.game_data.game_duration
            }
        }
    
    def __str__(self) -> str:
        return f"GameStateManager(current={self.current_state.name}, previous={self.previous_state.name if self.previous_state else None})"
