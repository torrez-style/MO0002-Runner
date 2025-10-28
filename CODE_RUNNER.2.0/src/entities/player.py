"""
Clase Jugador para el juego Maze Runner
Representa al jugador controlado por el usuario con funcionalidades avanzadas

MO0002 - Programación I - Universidad de Costa Rica
"""

from typing import Optional, Callable, List
from dataclasses import dataclass
from enum import Enum

from src.entities.character import Character, Position, Direction
from src.audio.sound_manager import sound_manager
from config.settings import settings


class PowerUpType(Enum):
    """Tipos de power-ups disponibles"""
    INVULNERABLE = "invulnerable"
    FREEZE_ENEMIES = "congelar"
    INVISIBLE = "invisible"


@dataclass
class PlayerStats:
    """Estadísticas del jugador"""
    lives: int = 3
    score: int = 0
    stars_collected: int = 0
    total_movements: int = 0
    enemies_avoided: int = 0
    powerups_used: int = 0
    levels_completed: int = 0


class Player(Character):
    """
    Representa al jugador controlado por el usuario
    Hereda de Character e implementa funcionalidades específicas del jugador
    """
    
    def __init__(self, 
                 name: str,
                 position: Position,
                 position_validator: Optional[Callable[[Position], bool]] = None):
        """
        Inicializa el jugador
        
        Args:
            name: Nombre del jugador
            position: Posición inicial
            position_validator: Función para validar posiciones
        """
        # Validaciones de entrada
        if not isinstance(name, str):
            raise ValueError("El nombre debe ser un string")
        if not name.strip():
            raise ValueError("El nombre no puede estar vacío")
        if len(name.strip()) > 50:
            raise ValueError("El nombre no puede exceder 50 caracteres")
        
        super().__init__(position, position_validator)
        
        # Atributos específicos del jugador
        self._name = name.strip()
        self._stats = PlayerStats()
        self._current_direction = Direction.NONE
        self._last_direction = Direction.NONE
        
        # Sistema de power-ups
        self._active_powerup: Optional[PowerUpType] = None
        self._powerup_timer = 0
        self._powerup_duration = settings.POWERUP_DURATION
        
        # Sistema de movimiento suave
        self._movement_delay = settings.PLAYER_STEP_DELAY
        self._movement_timer = 0
        
        # Callbacks para eventos
        self._on_star_collected_callbacks: List[Callable] = []
        self._on_powerup_activated_callbacks: List[Callable] = []
        self._on_life_lost_callbacks: List[Callable] = []
        
        print(f"🎮 Jugador creado: {self._name}")
    
    # === PROPIEDADES ===
    
    @property
    def name(self) -> str:
        """Nombre del jugador"""
        return self._name
    
    @property
    def lives(self) -> int:
        """Vidas restantes"""
        return self._stats.lives
    
    @property
    def score(self) -> int:
        """Puntuación actual"""
        return self._stats.score
    
    @property
    def stars_collected(self) -> int:
        """Estrellas recolectadas"""
        return self._stats.stars_collected
    
    @property
    def current_direction(self) -> Direction:
        """Dirección actual de movimiento"""
        return self._current_direction
    
    @property
    def active_powerup(self) -> Optional[PowerUpType]:
        """Power-up activo actualmente"""
        return self._active_powerup
    
    @property
    def powerup_timer(self) -> int:
        """Tiempo restante del power-up activo"""
        return self._powerup_timer
    
    @property
    def is_invulnerable(self) -> bool:
        """Indica si el jugador es invulnerable"""
        return self._active_powerup == PowerUpType.INVULNERABLE
    
    @property
    def is_invisible(self) -> bool:
        """Indica si el jugador es invisible"""
        return self._active_powerup == PowerUpType.INVISIBLE
    
    @property
    def stats(self) -> PlayerStats:
        """Estadísticas completas del jugador"""
        return self._stats
    
    # === MÉTODOS DE MOVIMIENTO ===
    
    def move(self, direction: Direction, validate: bool = True) -> bool:
        """
        Mueve el jugador en la dirección especificada
        
        Args:
            direction: Dirección de movimiento
            validate: Si debe validar el movimiento
        
        Returns:
            True si se pudo mover, False si no
        """
        if not self._is_active or self._movement_timer > 0:
            return False
        
        # Intentar el movimiento
        if super().move(direction, validate):
            self._current_direction = direction
            self._last_direction = direction
            self._movement_timer = self._movement_delay
            
            # Actualizar estadísticas
            self._stats.total_movements += 1
            
            # Añadir puntos por movimiento
            self.add_score(settings.POINTS_PER_MOVE)
            
            # Reproducir sonido de movimiento
            sound_manager.play_move()
            
            return True
        
        return False
    
    def try_move_direction(self, direction: Direction) -> bool:
        """
        Intenta mover en una dirección específica
        Usado para input del usuario
        """
        return self.move(direction, validate=True)
    
    def update(self, delta_time: float) -> None:
        """
        Actualiza el estado del jugador
        
        Args:
            delta_time: Tiempo transcurrido desde la última actualización
        """
        # Actualizar timer de movimiento
        if self._movement_timer > 0:
            self._movement_timer = max(0, self._movement_timer - 1)
        
        # Actualizar power-up
        if self._active_powerup and self._powerup_timer > 0:
            self._powerup_timer -= 1
            
            if self._powerup_timer <= 0:
                self._deactivate_powerup()
    
    # === SISTEMA DE PUNTUACIÓN ===
    
    def add_score(self, points: int) -> None:
        """
        Añade puntos al jugador
        
        Args:
            points: Puntos a añadir (debe ser positivo)
        """
        if not isinstance(points, int) or points < 0:
            raise ValueError("Los puntos deben ser un entero no negativo")
        
        self._stats.score += points
        print(f"💯 +{points} puntos. Total: {self._stats.score}")
    
    def collect_star(self) -> None:
        """
        Recolecta una estrella
        Añade puntos y actualiza estadísticas
        """
        self._stats.stars_collected += 1
        self.add_score(settings.POINTS_PER_ITEM)
        
        # Reproducir sonido de estrella
        sound_manager.play_star()
        
        # Ejecutar callbacks
        for callback in self._on_star_collected_callbacks:
            callback(self._stats.stars_collected)
        
        print(f"⭐ Estrella recolectada! Total: {self._stats.stars_collected}")
    
    # === SISTEMA DE VIDAS ===
    
    def lose_life(self) -> bool:
        """
        El jugador pierde una vida
        
        Returns:
            True si perdió la última vida (Game Over), False si no
        """
        if self._stats.lives > 0:
            self._stats.lives -= 1
            
            # Reproducir sonido de daño
            sound_manager.play_hit()
            
            # Ejecutar callbacks
            for callback in self._on_life_lost_callbacks:
                callback(self._stats.lives)
            
            is_game_over = self._stats.lives == 0
            
            if is_game_over:
                print(f"💀 Game Over para {self._name}")
                self.deactivate()
            else:
                print(f"❤️  Vida perdida. Vidas restantes: {self._stats.lives}")
            
            return is_game_over
        
        return True  # Ya estaba en 0 vidas
    
    def add_life(self) -> None:
        """Añade una vida extra al jugador"""
        self._stats.lives += 1
        print(f"❤️  Vida extra! Total: {self._stats.lives}")
    
    # === SISTEMA DE POWER-UPS ===
    
    def activate_powerup(self, powerup_type: PowerUpType) -> None:
        """
        Activa un power-up
        
        Args:
            powerup_type: Tipo de power-up a activar
        """
        if not isinstance(powerup_type, PowerUpType):
            raise ValueError("Tipo de power-up inválido")
        
        # Desactivar power-up anterior si existe
        if self._active_powerup:
            self._deactivate_powerup()
        
        self._active_powerup = powerup_type
        self._powerup_timer = self._powerup_duration
        self._stats.powerups_used += 1
        
        # Ejecutar callbacks
        for callback in self._on_powerup_activated_callbacks:
            callback(powerup_type)
        
        print(f"✨ Power-up activado: {powerup_type.value}")
    
    def _deactivate_powerup(self) -> None:
        """Desactiva el power-up actual"""
        if self._active_powerup:
            print(f"⏰ Power-up expirado: {self._active_powerup.value}")
            self._active_powerup = None
            self._powerup_timer = 0
    
    def has_powerup(self, powerup_type: PowerUpType) -> bool:
        """Verifica si tiene un power-up específico activo"""
        return self._active_powerup == powerup_type
    
    # === CALLBACKS Y EVENTOS ===
    
    def register_star_collected_callback(self, callback: Callable[[int], None]) -> None:
        """Registra callback para cuando se recolecta una estrella"""
        self._on_star_collected_callbacks.append(callback)
    
    def register_powerup_activated_callback(self, callback: Callable[[PowerUpType], None]) -> None:
        """Registra callback para cuando se activa un power-up"""
        self._on_powerup_activated_callbacks.append(callback)
    
    def register_life_lost_callback(self, callback: Callable[[int], None]) -> None:
        """Registra callback para cuando se pierde una vida"""
        self._on_life_lost_callbacks.append(callback)
    
    # === IMPLEMENTACIONES ABSTRACTAS ===
    
    def on_collision(self, other: 'Character') -> None:
        """
        Maneja la colisión con otro personaje
        
        Args:
            other: El otro personaje con el que colisionó
        """
        from src.entities.enemy import Enemy
        
        if isinstance(other, Enemy) and not self.is_invulnerable:
            # Colisión con enemigo sin ser invulnerable
            self.lose_life()
            print(f"💥 {self._name} colisionó con enemigo en {other.position}")
    
    def on_move(self, direction: Direction) -> None:
        """Callback ejecutado cuando el jugador se mueve"""
        # Aquí se pueden añadir efectos de sonido adicionales
        pass
    
    def on_activate(self) -> None:
        """Callback ejecutado cuando el jugador se activa"""
        print(f"🎮 {self._name} activado")
    
    def on_deactivate(self) -> None:
        """Callback ejecutado cuando el jugador se desactiva"""
        print(f"💤 {self._name} desactivado")
    
    def on_reset(self) -> None:
        """Callback ejecutado cuando se reinicia la posición del jugador"""
        self._current_direction = Direction.NONE
        self._movement_timer = 0
        print(f"🔄 Posición de {self._name} reiniciada")
    
    # === MÉTODOS DE UTILIDAD ===
    
    def reset_stats(self) -> None:
        """Reinicia las estadísticas del jugador"""
        self._stats = PlayerStats()
        self._active_powerup = None
        self._powerup_timer = 0
        print(f"📊 Estadísticas de {self._name} reiniciadas")
    
    def get_game_summary(self) -> str:
        """
        Obtiene un resumen del desempeño del jugador
        
        Returns:
            Resumen en formato string
        """
        return f"""
=== RESUMEN DE {self._name.upper()} ===
Puntuación Final: {self._stats.score:,}
Vidas Restantes: {self._stats.lives}
Estrellas Recolectadas: {self._stats.stars_collected}
Movimientos Totales: {self._stats.total_movements}
Power-ups Usados: {self._stats.powerups_used}
Niveles Completados: {self._stats.levels_completed}
        """.strip()
    
    def get_detailed_info(self) -> dict:
        """Obtiene información detallada del jugador"""
        info = super().get_info()
        info.update({
            'name': self._name,
            'lives': self._stats.lives,
            'score': self._stats.score,
            'stars_collected': self._stats.stars_collected,
            'current_direction': self._current_direction.name,
            'active_powerup': self._active_powerup.value if self._active_powerup else None,
            'powerup_timer': self._powerup_timer,
            'total_movements': self._stats.total_movements,
            'powerups_used': self._stats.powerups_used,
            'levels_completed': self._stats.levels_completed
        })
        return info
    
    def __str__(self) -> str:
        powerup_str = f" ({self._active_powerup.value})" if self._active_powerup else ""
        return f"Player({self._name}, pos={self._position}, lives={self._stats.lives}, score={self._stats.score}{powerup_str})"
