"""
Sistema de gestión de eventos para Maze Runner
Implementa el patrón Observer con tipado fuerte y validaciones

MO0002 - Programación I - Universidad de Costa Rica
"""

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Dict, List, Callable, Any, Optional, Type, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime
import weakref
import logging


class EventType(Enum):
    """Tipos de eventos del juego"""
    # Eventos del jugador
    PLAYER_MOVED = auto()
    PLAYER_STAR_COLLECTED = auto()
    PLAYER_POWERUP_ACTIVATED = auto()
    PLAYER_LIFE_LOST = auto()
    PLAYER_RESPAWNED = auto()
    
    # Eventos de enemigos
    ENEMY_PLAYER_COLLISION = auto()
    ENEMY_STATE_CHANGED = auto()
    ENEMY_TARGET_ACQUIRED = auto()
    
    # Eventos del juego
    GAME_STARTED = auto()
    GAME_PAUSED = auto()
    GAME_RESUMED = auto()
    GAME_OVER = auto()
    LEVEL_COMPLETED = auto()
    LEVEL_STARTED = auto()
    
    # Eventos de menú
    MENU_OPTION_SELECTED = auto()
    MENU_STATE_CHANGED = auto()
    
    # Eventos de audio
    SOUND_EFFECT_REQUESTED = auto()
    MUSIC_CHANGE_REQUESTED = auto()
    
    # Eventos del sistema
    SETTINGS_CHANGED = auto()
    FILE_LOADED = auto()
    ERROR_OCCURRED = auto()


@dataclass
class GameEvent:
    """
    Clase base para todos los eventos del juego
    Contiene información común a todos los eventos
    """
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    source: Optional[str] = None  # Quién generó el evento
    data: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        source_str = f" from {self.source}" if self.source else ""
        return f"GameEvent({self.event_type.name}{source_str}) at {self.timestamp.strftime('%H:%M:%S')}"


# Eventos específicos del juego

@dataclass
class PlayerMovedEvent(GameEvent):
    """Evento cuando el jugador se mueve"""
    from_position: tuple[int, int] = (0, 0)
    to_position: tuple[int, int] = (0, 0)
    direction: str = ""
    
    def __post_init__(self):
        self.event_type = EventType.PLAYER_MOVED
        self.data.update({
            'from_position': self.from_position,
            'to_position': self.to_position,
            'direction': self.direction
        })


@dataclass
class PlayerStarCollectedEvent(GameEvent):
    """Evento cuando el jugador recolecta una estrella"""
    star_position: tuple[int, int] = (0, 0)
    points_gained: int = 0
    total_stars: int = 0
    
    def __post_init__(self):
        self.event_type = EventType.PLAYER_STAR_COLLECTED
        self.data.update({
            'star_position': self.star_position,
            'points_gained': self.points_gained,
            'total_stars': self.total_stars
        })


@dataclass
class PlayerPowerUpActivatedEvent(GameEvent):
    """Evento cuando se activa un power-up"""
    powerup_type: str = ""
    duration: int = 0
    player_position: tuple[int, int] = (0, 0)
    
    def __post_init__(self):
        self.event_type = EventType.PLAYER_POWERUP_ACTIVATED
        self.data.update({
            'powerup_type': self.powerup_type,
            'duration': self.duration,
            'player_position': self.player_position
        })


@dataclass
class EnemyPlayerCollisionEvent(GameEvent):
    """Evento cuando un enemigo colisiona con el jugador"""
    enemy_position: tuple[int, int] = (0, 0)
    player_position: tuple[int, int] = (0, 0)
    player_invulnerable: bool = False
    
    def __post_init__(self):
        self.event_type = EventType.ENEMY_PLAYER_COLLISION
        self.data.update({
            'enemy_position': self.enemy_position,
            'player_position': self.player_position,
            'player_invulnerable': self.player_invulnerable
        })


@dataclass
class GameStateEvent(GameEvent):
    """Evento para cambios de estado del juego"""
    old_state: str = ""
    new_state: str = ""
    additional_data: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.data.update({
            'old_state': self.old_state,
            'new_state': self.new_state,
            'additional_data': self.additional_data
        })


@dataclass
class MenuSelectionEvent(GameEvent):
    """Evento cuando se selecciona una opción del menú"""
    selected_option: str = ""
    menu_type: str = ""
    
    def __post_init__(self):
        self.event_type = EventType.MENU_OPTION_SELECTED
        self.data.update({
            'selected_option': self.selected_option,
            'menu_type': self.menu_type
        })


@dataclass
class SoundEffectEvent(GameEvent):
    """Evento para solicitar efectos de sonido"""
    sound_name: str = ""
    volume_multiplier: float = 1.0
    
    def __post_init__(self):
        self.event_type = EventType.SOUND_EFFECT_REQUESTED
        self.data.update({
            'sound_name': self.sound_name,
            'volume_multiplier': self.volume_multiplier
        })


# Interfaz para observadores
class EventObserver(ABC):
    """Interfaz abstracta para observadores de eventos"""
    
    @abstractmethod
    def handle_event(self, event: GameEvent) -> None:
        """Maneja un evento recibido"""
        pass
    
    def get_observed_events(self) -> List[EventType]:
        """Retorna los tipos de eventos que este observador maneja"""
        return []  # Override en subclases


# Tipos genéricos para callbacks
T = TypeVar('T', bound=GameEvent)
EventCallback = Callable[[T], None]


class EventManager:
    """
    Administrador centralizado de eventos del juego
    Implementa el patrón Observer con funcionalidades avanzadas
    """
    
    def __init__(self, enable_logging: bool = True):
        """Inicializa el administrador de eventos"""
        # Almacenamiento de observadores por tipo de evento
        self._observers: Dict[EventType, List[EventObserver]] = {}
        self._callbacks: Dict[EventType, List[EventCallback]] = {}
        
        # Sistema de weak references para evitar memory leaks
        self._weak_observers: Dict[EventType, List[weakref.ref]] = {}
        
        # Cola de eventos para procesamiento diferido
        self._event_queue: List[GameEvent] = []
        self._processing_queue = False
        
        # Estadísticas y debugging
        self._event_count: Dict[EventType, int] = {}
        self._total_events_processed = 0
        self._enable_logging = enable_logging
        
        # Filtros de eventos
        self._event_filters: List[Callable[[GameEvent], bool]] = []
        
        # Inicializar contadores
        for event_type in EventType:
            self._observers[event_type] = []
            self._callbacks[event_type] = []
            self._weak_observers[event_type] = []
            self._event_count[event_type] = 0
        
        if self._enable_logging:
            logging.basicConfig(level=logging.INFO)
            self._logger = logging.getLogger('EventManager')
            self._logger.info("📡 EventManager inicializado")
    
    def subscribe(self, event_type: EventType, observer: EventObserver) -> None:
        """
        Suscribe un observador a un tipo de evento
        
        Args:
            event_type: Tipo de evento a observar
            observer: Observador que manejara el evento
        """
        if not isinstance(observer, EventObserver):
            raise TypeError("El observador debe implementar EventObserver")
        
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)
            
            # Crear weak reference para evitar memory leaks
            weak_ref = weakref.ref(observer, 
                                  lambda ref: self._cleanup_weak_reference(event_type, ref))
            self._weak_observers[event_type].append(weak_ref)
            
            if self._enable_logging:
                self._logger.info(f"🔔 {observer.__class__.__name__} suscrito a {event_type.name}")
    
    def subscribe_callback(self, event_type: EventType, callback: EventCallback) -> None:
        """
        Suscribe un callback a un tipo de evento
        
        Args:
            event_type: Tipo de evento
            callback: Función callback a ejecutar
        """
        if not callable(callback):
            raise TypeError("El callback debe ser callable")
        
        self._callbacks[event_type].append(callback)
        
        if self._enable_logging:
            self._logger.info(f"🔔 Callback suscrito a {event_type.name}")
    
    def unsubscribe(self, event_type: EventType, observer: EventObserver) -> bool:
        """
        Desuscribe un observador de un tipo de evento
        
        Args:
            event_type: Tipo de evento
            observer: Observador a desuscribir
        
        Returns:
            True si se desusbcribió exitosamente
        """
        try:
            self._observers[event_type].remove(observer)
            if self._enable_logging:
                self._logger.info(f"🔕 {observer.__class__.__name__} desuscrito de {event_type.name}")
            return True
        except ValueError:
            return False
    
    def publish(self, event: GameEvent) -> None:
        """
        Publica un evento a todos los observadores suscritos
        
        Args:
            event: Evento a publicar
        """
        if not isinstance(event, GameEvent):
            raise TypeError("El evento debe ser una instancia de GameEvent")
        
        # Aplicar filtros
        for event_filter in self._event_filters:
            if not event_filter(event):
                return  # Evento filtrado
        
        # Añadir a cola si estamos procesando
        if self._processing_queue:
            self._event_queue.append(event)
            return
        
        self._process_event(event)
    
    def publish_immediate(self, event: GameEvent) -> None:
        """
        Publica un evento inmediatamente, saltando la cola
        
        Args:
            event: Evento a publicar inmediatamente
        """
        self._process_event(event)
    
    def queue_event(self, event: GameEvent) -> None:
        """
        Añade un evento a la cola para procesamiento diferido
        
        Args:
            event: Evento a añadir a la cola
        """
        self._event_queue.append(event)
    
    def process_queued_events(self) -> int:
        """
        Procesa todos los eventos en cola
        
        Returns:
            Número de eventos procesados
        """
        if self._processing_queue:
            return 0  # Ya estamos procesando
        
        self._processing_queue = True
        processed_count = 0
        
        try:
            while self._event_queue:
                event = self._event_queue.pop(0)
                self._process_event(event)
                processed_count += 1
        finally:
            self._processing_queue = False
        
        return processed_count
    
    def _process_event(self, event: GameEvent) -> None:
        """Procesa un evento individual"""
        event_type = event.event_type
        
        # Actualizar estadísticas
        self._event_count[event_type] += 1
        self._total_events_processed += 1
        
        if self._enable_logging:
            self._logger.debug(f"📡 Procesando {event}")
        
        # Limpiar weak references muertas
        self._cleanup_dead_weak_references(event_type)
        
        # Notificar observadores
        for observer in self._observers[event_type].copy():  # Copy to avoid modification during iteration
            try:
                observer.handle_event(event)
            except Exception as e:
                if self._enable_logging:
                    self._logger.error(f"❌ Error en observador {observer.__class__.__name__}: {e}")
        
        # Ejecutar callbacks
        for callback in self._callbacks[event_type].copy():
            try:
                callback(event)
            except Exception as e:
                if self._enable_logging:
                    self._logger.error(f"❌ Error en callback: {e}")
    
    def add_event_filter(self, filter_func: Callable[[GameEvent], bool]) -> None:
        """
        Añade un filtro de eventos
        
        Args:
            filter_func: Función que retorna True si el evento debe procesarse
        """
        if callable(filter_func):
            self._event_filters.append(filter_func)
    
    def remove_event_filter(self, filter_func: Callable[[GameEvent], bool]) -> bool:
        """
        Remueve un filtro de eventos
        
        Args:
            filter_func: Filtro a remover
        
        Returns:
            True si se removió exitosamente
        """
        try:
            self._event_filters.remove(filter_func)
            return True
        except ValueError:
            return False
    
    def _cleanup_dead_weak_references(self, event_type: EventType) -> None:
        """Limpia weak references que ya no son válidas"""
        alive_refs = []
        for weak_ref in self._weak_observers[event_type]:
            if weak_ref() is not None:  # Reference still alive
                alive_refs.append(weak_ref)
        self._weak_observers[event_type] = alive_refs
    
    def _cleanup_weak_reference(self, event_type: EventType, dead_ref: weakref.ref) -> None:
        """Callback para limpiar una weak reference muerta"""
        try:
            self._weak_observers[event_type].remove(dead_ref)
        except ValueError:
            pass  # Ya fue removida
    
    def clear_all_subscriptions(self) -> None:
        """Limpia todas las suscripciones"""
        for event_type in EventType:
            self._observers[event_type].clear()
            self._callbacks[event_type].clear()
            self._weak_observers[event_type].clear()
        
        if self._enable_logging:
            self._logger.info("🧼 Todas las suscripciones limpiadas")
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtiene estadísticas del administrador de eventos"""
        return {
            'total_events_processed': self._total_events_processed,
            'events_by_type': dict(self._event_count),
            'active_observers': {et.name: len(obs) for et, obs in self._observers.items() if obs},
            'active_callbacks': {et.name: len(cb) for et, cb in self._callbacks.items() if cb},
            'queued_events': len(self._event_queue),
            'event_filters': len(self._event_filters)
        }
    
    def reset_statistics(self) -> None:
        """Reinicia las estadísticas"""
        for event_type in EventType:
            self._event_count[event_type] = 0
        self._total_events_processed = 0
        
        if self._enable_logging:
            self._logger.info("📊 Estadísticas reiniciadas")
    
    def __str__(self) -> str:
        active_subs = sum(len(obs) for obs in self._observers.values())
        return f"EventManager(subscribers={active_subs}, processed={self._total_events_processed}, queued={len(self._event_queue)})"
