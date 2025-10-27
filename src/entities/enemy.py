"""
Clase Enemy para el juego Maze Runner
Representa enemigos con IA avanzada que persiguen al jugador

MO0002 - Programación I - Universidad de Costa Rica
"""

from typing import Optional, Callable, List, Tuple, Set
from collections import deque
from enum import Enum
from dataclasses import dataclass
import random

from src.entities.character import Character, Position, Direction
from config.settings import settings


class EnemyState(Enum):
    """Estados posibles del enemigo"""
    IDLE = "idle"          # Inactivo
    PATROLLING = "patrolling"  # Patrullando
    CHASING = "chasing"    # Persiguiendo al jugador
    FROZEN = "frozen"      # Congelado por power-up
    CONFUSED = "confused"  # Confundido (jugador invisible)


class AIBehavior(Enum):
    """Tipos de comportamiento de IA"""
    AGGRESSIVE = "aggressive"    # Persigue directamente
    SMART = "smart"             # Usa pathfinding BFS
    PATROL = "patrol"           # Patrulla área
    RANDOM = "random"           # Movimiento aleatorio


@dataclass
class EnemyStats:
    """Estadísticas del enemigo"""
    moves_made: int = 0
    player_catches: int = 0
    times_frozen: int = 0
    pathfinding_calculations: int = 0


class Enemy(Character):
    """
    Representa un enemigo inteligente que persigue al jugador
    Implementa diferentes tipos de IA según la dificultad
    """
    
    def __init__(self, 
                 position: Position,
                 ai_behavior: AIBehavior = AIBehavior.SMART,
                 speed_multiplier: float = 1.0,
                 position_validator: Optional[Callable[[Position], bool]] = None):
        """
        Inicializa el enemigo
        
        Args:
            position: Posición inicial
            ai_behavior: Tipo de comportamiento de IA
            speed_multiplier: Multiplicador de velocidad
            position_validator: Función para validar posiciones
        """
        super().__init__(position, position_validator)
        
        # Configuración de IA
        self._ai_behavior = ai_behavior
        self._speed_multiplier = max(0.1, speed_multiplier)
        self._base_speed = settings.ENEMY_SPEED_BASE
        self._movement_delay = max(1, int(self._base_speed / self._speed_multiplier))
        
        # Estado del enemigo
        self._state = EnemyState.PATROLLING
        self._last_state = EnemyState.IDLE
        self._movement_timer = 0
        
        # Sistema de targeting
        self._target_position: Optional[Position] = None
        self._last_known_player_position: Optional[Position] = None
        self._detection_range = 10  # Rango de detección
        
        # Pathfinding y navegación
        self._path_cache: List[Position] = []
        self._path_cache_target: Optional[Position] = None
        self._stuck_counter = 0
        self._max_stuck_moves = 5
        
        # Sistema de patrullaje
        self._patrol_points: List[Position] = []
        self._current_patrol_index = 0
        self._patrol_radius = 5
        
        # Timers para estados especiales
        self._frozen_timer = 0
        self._confusion_timer = 0
        
        # Estadísticas
        self._stats = EnemyStats()
        
        # Referencias externas
        self._maze_grid: Optional[List[List[int]]] = None
        self._other_enemies: List['Enemy'] = []
        
        print(f"👾 Enemigo creado en {position} con IA {ai_behavior.value}")
    
    # === PROPIEDADES ===
    
    @property
    def state(self) -> EnemyState:
        """Estado actual del enemigo"""
        return self._state
    
    @property
    def ai_behavior(self) -> AIBehavior:
        """Comportamiento de IA actual"""
        return self._ai_behavior
    
    @property
    def target_position(self) -> Optional[Position]:
        """Posición objetivo actual"""
        return self._target_position
    
    @property
    def is_frozen(self) -> bool:
        """Indica si el enemigo está congelado"""
        return self._state == EnemyState.FROZEN
    
    @property
    def is_chasing(self) -> bool:
        """Indica si el enemigo está persiguiendo"""
        return self._state == EnemyState.CHASING
    
    @property
    def stats(self) -> EnemyStats:
        """Estadísticas del enemigo"""
        return self._stats
    
    # === CONFIGURACIÓN ===
    
    def set_maze_grid(self, maze_grid: List[List[int]]) -> None:
        """Establece la cuadrícula del laberinto para pathfinding"""
        self._maze_grid = maze_grid
    
    def set_other_enemies(self, enemies: List['Enemy']) -> None:
        """Establece lista de otros enemigos para evitar colisiones"""
        self._other_enemies = [e for e in enemies if e != self]
    
    def set_ai_behavior(self, behavior: AIBehavior) -> None:
        """Cambia el comportamiento de IA"""
        self._ai_behavior = behavior
        self._path_cache.clear()  # Limpiar cache de pathfinding
        print(f"🤖 IA cambiada a {behavior.value}")
    
    # === ACTUALIZACIÓN ===
    
    def update(self, delta_time: float) -> None:
        """
        Actualiza el estado del enemigo
        
        Args:
            delta_time: Tiempo transcurrido desde la última actualización
        """
        if not self._is_active:
            return
        
        # Actualizar timers
        self._update_timers()
        
        # Actualizar estado
        self._update_state()
        
        # Procesar movimiento según el timer
        if self._movement_timer <= 0:
            if self._state != EnemyState.FROZEN:
                self._process_movement()
            self._movement_timer = self._movement_delay
        else:
            self._movement_timer -= 1
    
    def _update_timers(self) -> None:
        """Actualiza todos los timers del enemigo"""
        if self._frozen_timer > 0:
            self._frozen_timer -= 1
            if self._frozen_timer == 0:
                self._unfreeze()
        
        if self._confusion_timer > 0:
            self._confusion_timer -= 1
            if self._confusion_timer == 0 and self._state == EnemyState.CONFUSED:
                self._state = EnemyState.PATROLLING
    
    def _update_state(self) -> None:
        """Actualiza el estado del enemigo según las condiciones"""
        if self._state == EnemyState.FROZEN:
            return  # No cambiar estado mientras esté congelado
        
        # Transiciones de estado basadas en condiciones
        if self._target_position and self._state != EnemyState.CONFUSED:
            distance = self._position.distance_to(self._target_position)
            
            if distance <= self._detection_range:
                if self._state != EnemyState.CHASING:
                    self._state = EnemyState.CHASING
                    print(f"🎯 Enemigo en {self._position} comenzó a perseguir")
            elif self._state == EnemyState.CHASING:
                self._state = EnemyState.PATROLLING
                print(f"🚫 Enemigo en {self._position} perdió el objetivo")
    
    def _process_movement(self) -> None:
        """Procesa el movimiento según el comportamiento de IA"""
        next_position = None
        
        if self._ai_behavior == AIBehavior.SMART:
            next_position = self._smart_movement()
        elif self._ai_behavior == AIBehavior.AGGRESSIVE:
            next_position = self._aggressive_movement()
        elif self._ai_behavior == AIBehavior.PATROL:
            next_position = self._patrol_movement()
        elif self._ai_behavior == AIBehavior.RANDOM:
            next_position = self._random_movement()
        
        # Intentar el movimiento
        if next_position and self._attempt_move(next_position):
            self._stats.moves_made += 1
            self._stuck_counter = 0
        else:
            self._stuck_counter += 1
            if self._stuck_counter >= self._max_stuck_moves:
                self._handle_stuck_situation()
    
    def _smart_movement(self) -> Optional[Position]:
        """Movimiento inteligente usando pathfinding BFS"""
        if not self._target_position or not self._maze_grid:
            return self._random_movement()
        
        # Usar cache si el objetivo no ha cambiado
        if (self._path_cache and 
            self._path_cache_target == self._target_position and
            len(self._path_cache) > 1):
            return self._path_cache[1]  # Siguiente paso en el path
        
        # Calcular nuevo path
        path = self._calculate_bfs_path(self._position, self._target_position)
        self._stats.pathfinding_calculations += 1
        
        if path and len(path) > 1:
            self._path_cache = path
            self._path_cache_target = self._target_position
            return path[1]  # Siguiente paso
        
        # Fallback a movimiento agresivo
        return self._aggressive_movement()
    
    def _aggressive_movement(self) -> Optional[Position]:
        """Movimiento agresivo directo hacia el objetivo"""
        if not self._target_position:
            return self._random_movement()
        
        dx = self._target_position.x - self._position.x
        dy = self._target_position.y - self._position.y
        
        # Determinar dirección preferida
        directions = []
        if dx > 0:
            directions.append(Direction.RIGHT)
        elif dx < 0:
            directions.append(Direction.LEFT)
        
        if dy > 0:
            directions.append(Direction.DOWN)
        elif dy < 0:
            directions.append(Direction.UP)
        
        # Intentar direcciones en orden de prioridad
        for direction in directions:
            new_pos = self._position.move(direction)
            if self._is_valid_move(new_pos):
                return new_pos
        
        # Fallback a movimiento aleatorio
        return self._random_movement()
    
    def _patrol_movement(self) -> Optional[Position]:
        """Movimiento de patrullaje entre puntos predefinidos"""
        if not self._patrol_points:
            self._generate_patrol_points()
        
        if not self._patrol_points:
            return self._random_movement()
        
        target_patrol = self._patrol_points[self._current_patrol_index]
        
        # Si llegamos al punto de patrulla, cambiar al siguiente
        if self._position.distance_to(target_patrol) <= 1.0:
            self._current_patrol_index = (self._current_patrol_index + 1) % len(self._patrol_points)
            target_patrol = self._patrol_points[self._current_patrol_index]
        
        # Mover hacia el punto de patrulla
        dx = target_patrol.x - self._position.x
        dy = target_patrol.y - self._position.y
        
        if abs(dx) > abs(dy):
            direction = Direction.RIGHT if dx > 0 else Direction.LEFT
        else:
            direction = Direction.DOWN if dy > 0 else Direction.UP
        
        new_pos = self._position.move(direction)
        return new_pos if self._is_valid_move(new_pos) else self._random_movement()
    
    def _random_movement(self) -> Optional[Position]:
        """Movimiento aleatorio"""
        directions = [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]
        random.shuffle(directions)
        
        for direction in directions:
            new_pos = self._position.move(direction)
            if self._is_valid_move(new_pos):
                return new_pos
        
        return None  # No hay movimientos válidos
    
    def _calculate_bfs_path(self, start: Position, target: Position) -> List[Position]:
        """Calcula el camino óptimo usando BFS"""
        if not self._maze_grid:
            return []
        
        queue = deque([(start, [start])])
        visited: Set[Tuple[int, int]] = {start.as_tuple()}
        
        while queue:
            current_pos, path = queue.popleft()
            
            if current_pos == target:
                return path
            
            # Explorar direcciones adyacentes
            for direction in [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]:
                next_pos = current_pos.move(direction)
                next_tuple = next_pos.as_tuple()
                
                if (next_tuple not in visited and 
                    self._is_valid_position_for_pathfinding(next_pos)):
                    
                    visited.add(next_tuple)
                    queue.append((next_pos, path + [next_pos]))
        
        return []  # No se encontró camino
    
    def _is_valid_move(self, position: Position) -> bool:
        """Verifica si un movimiento es válido"""
        # Verificar validador de posición
        if self._position_validator and not self._position_validator(position):
            return False
        
        # Verificar colisión con otros enemigos
        for enemy in self._other_enemies:
            if enemy.position == position:
                return False
        
        return True
    
    def _is_valid_position_for_pathfinding(self, position: Position) -> bool:
        """Verifica si una posición es válida para pathfinding"""
        if not self._maze_grid:
            return True
        
        if (position.y < 0 or position.y >= len(self._maze_grid) or
            position.x < 0 or position.x >= len(self._maze_grid[0])):
            return False
        
        # 0 = espacio libre, 1 = pared
        return self._maze_grid[position.y][position.x] != 1
    
    def _attempt_move(self, new_position: Position) -> bool:
        """Intenta mover a una nueva posición"""
        if self._is_valid_move(new_position):
            self.set_position(new_position, validate=False)
            return True
        return False
    
    def _handle_stuck_situation(self) -> None:
        """Maneja la situación cuando el enemigo está atascado"""
        print(f"🚫 Enemigo atascado en {self._position}, cambiando estrategia")
        
        # Limpiar cache de pathfinding
        self._path_cache.clear()
        
        # Cambiar temporalmente a movimiento aleatorio
        original_behavior = self._ai_behavior
        self._ai_behavior = AIBehavior.RANDOM
        
        # Intentar movimiento aleatorio
        random_pos = self._random_movement()
        if random_pos:
            self._attempt_move(random_pos)
        
        # Restaurar comportamiento original
        self._ai_behavior = original_behavior
        self._stuck_counter = 0
    
    def _generate_patrol_points(self) -> None:
        """Genera puntos de patrulla alrededor de la posición inicial"""
        if not self._maze_grid:
            return
        
        base_x, base_y = self._position.x, self._position.y
        
        for _ in range(8):  # Intentar generar 8 puntos
            for _ in range(10):  # Máximo 10 intentos por punto
                x = base_x + random.randint(-self._patrol_radius, self._patrol_radius)
                y = base_y + random.randint(-self._patrol_radius, self._patrol_radius)
                pos = Position(x, y)
                
                if (self._is_valid_position_for_pathfinding(pos) and 
                    pos not in self._patrol_points):
                    self._patrol_points.append(pos)
                    break
        
        if not self._patrol_points:
            self._patrol_points.append(self._position)  # Fallback
    
    # === CONTROL DE ESTADOS ESPECIALES ===
    
    def freeze(self, duration: int) -> None:
        """Congela al enemigo por un tiempo determinado"""
        self._last_state = self._state
        self._state = EnemyState.FROZEN
        self._frozen_timer = duration
        self._stats.times_frozen += 1
        print(f"❄️  Enemigo congelado por {duration} frames")
    
    def _unfreeze(self) -> None:
        """Descongela al enemigo"""
        self._state = self._last_state
        print(f"🔥 Enemigo descongelado")
    
    def confuse(self, duration: int) -> None:
        """Confunde al enemigo (para cuando el jugador es invisible)"""
        self._state = EnemyState.CONFUSED
        self._confusion_timer = duration
        self._target_position = None
        print(f"😵‍💫 Enemigo confundido por {duration} frames")
    
    # === TARGETING ===
    
    def set_target(self, target_position: Optional[Position]) -> None:
        """Establece la posición objetivo del enemigo"""
        self._target_position = target_position
        if target_position:
            self._last_known_player_position = Position(target_position.x, target_position.y)
    
    def clear_target(self) -> None:
        """Limpia el objetivo actual"""
        self._target_position = None
        self._path_cache.clear()
    
    # === IMPLEMENTACIONES ABSTRACTAS ===
    
    def on_collision(self, other: 'Character') -> None:
        """
        Maneja la colisión con otro personaje
        
        Args:
            other: El otro personaje con el que colisionó
        """
        from src.entities.player import Player
        
        if isinstance(other, Player):
            self._stats.player_catches += 1
            print(f"🎯 Enemigo capturó jugador en {other.position}")
    
    def get_detailed_info(self) -> dict:
        """Obtiene información detallada del enemigo"""
        info = super().get_info()
        info.update({
            'state': self._state.value,
            'ai_behavior': self._ai_behavior.value,
            'target_position': self._target_position.as_tuple() if self._target_position else None,
            'frozen_timer': self._frozen_timer,
            'confusion_timer': self._confusion_timer,
            'moves_made': self._stats.moves_made,
            'player_catches': self._stats.player_catches,
            'pathfinding_calculations': self._stats.pathfinding_calculations
        })
        return info
    
    def __str__(self) -> str:
        target_str = f" -> {self._target_position}" if self._target_position else ""
        return f"Enemy({self._ai_behavior.value}, pos={self._position}, state={self._state.value}{target_str})"