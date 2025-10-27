"""
Módulo World - Mundo del juego
Contiene el sistema de eventos y elementos del mundo
"""

from .events import (
    EventManager, EventObserver, GameEvent, EventType,
    PlayerMovedEvent, PlayerStarCollectedEvent, PlayerPowerUpActivatedEvent,
    EnemyPlayerCollisionEvent, GameStateEvent, MenuSelectionEvent, SoundEffectEvent
)

__all__ = [
    'EventManager', 'EventObserver', 'GameEvent', 'EventType',
    'PlayerMovedEvent', 'PlayerStarCollectedEvent', 'PlayerPowerUpActivatedEvent',
    'EnemyPlayerCollisionEvent', 'GameStateEvent', 'MenuSelectionEvent', 'SoundEffectEvent'
]
