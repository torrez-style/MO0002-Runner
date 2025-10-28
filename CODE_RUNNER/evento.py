"""
Módulo de gestión de eventos para el juego Maze-Run.
Implementa un sistema de eventos basado en el patrón Observer.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Type, Any


class Evento(ABC):
    """Clase base abstracta para todos los eventos del juego."""
    pass


class EventoSalir(Evento):
    """Evento disparado cuando el usuario quiere salir del juego."""
    pass


class EventoMoverJugador(Evento):
    """Evento disparado cuando el jugador se mueve."""
    
    def __init__(self, direccion: str):
        """
        Args:
            direccion: Dirección del movimiento ('arriba', 'abajo', 'izquierda', 'derecha').
        """
        self.direccion = direccion


class EventoRecogerEstrella(Evento):
    """Evento disparado cuando el jugador recoge una estrella."""
    
    def __init__(self, posicion: tuple):
        """
        Args:
            posicion: Posición donde se recogió la estrella (tupla x, y).
        """
        self.posicion = posicion


class EventoColisionEnemigo(Evento):
    """Evento disparado cuando el jugador colisiona con un enemigo."""
    
    def __init__(self, posicion_jugador: tuple, posicion_enemigo: tuple):
        """
        Args:
            posicion_jugador: Posición del jugador (tupla x, y).
            posicion_enemigo: Posición del enemigo (tupla x, y).
        """
        self.posicion_jugador = posicion_jugador
        self.posicion_enemigo = posicion_enemigo


class EventoSeleccionMenu(Evento):
    """Evento disparado cuando se selecciona una opción del menú."""
    
    def __init__(self, opcion: str):
        """
        Args:
            opcion: Opción seleccionada del menú.
        """
        self.opcion = opcion


class EventoFinDeJuego(Evento):
    """Evento disparado cuando el juego termina."""
    
    def __init__(self, puntuacion_final: int):
        """
        Args:
            puntuacion_final: Puntuación final obtenida por el jugador.
        """
        self.puntuacion_final = puntuacion_final


class EventoPotenciadorRecogido(Evento):
    """Evento disparado cuando el jugador recoge un potenciador."""
    
    def __init__(self, tipo: str):
        """
        Args:
            tipo: Tipo de potenciador ('invulnerable', 'congelar', 'invisible').
        """
        self.tipo = tipo


class EventoSalirNivel(Evento):
    """Evento disparado cuando el jugador llega a la salida del nivel."""
    pass


class EscuchaEventos(ABC):
    """Interfaz para objetos que pueden escuchar eventos."""
    
    @abstractmethod
    def notificar(self, evento: Evento) -> None:
        """
        Método llamado cuando se produce un evento.
        
        Args:
            evento: El evento que se ha producido.
        """
        pass


class AdministradorEventos:
    """Administrador central de eventos del juego."""
    
    def __init__(self):
        """Inicializa el administrador de eventos."""
        self._escuchas: Dict[Type[Evento], List[EscuchaEventos]] = {}
    
    def registrar(self, tipo_evento: Type[Evento], escucha: EscuchaEventos) -> None:
        """
        Registra un escucha para un tipo de evento específico.
        
        Args:
            tipo_evento: Tipo de evento a escuchar.
            escucha: Objeto que escuchará el evento.
        """
        if tipo_evento not in self._escuchas:
            self._escuchas[tipo_evento] = []
        
        if escucha not in self._escuchas[tipo_evento]:
            self._escuchas[tipo_evento].append(escucha)
    
    def desregistrar(self, tipo_evento: Type[Evento], escucha: EscuchaEventos) -> None:
        """
        Desregistra un escucha de un tipo de evento.
        
        Args:
            tipo_evento: Tipo de evento del cual desregistrar.
            escucha: Objeto a desregistrar.
        """
        if tipo_evento in self._escuchas and escucha in self._escuchas[tipo_evento]:
            self._escuchas[tipo_evento].remove(escucha)
    
    def publicar(self, evento: Evento) -> None:
        """
        Publica un evento a todos los escuchas registrados.
        
        Args:
            evento: Evento a publicar.
        """
        tipo_evento = type(evento)
        
        if tipo_evento in self._escuchas:
            # Crear una copia de la lista para evitar problemas si se modifica durante la iteración
            escuchas = list(self._escuchas[tipo_evento])
            for escucha in escuchas:
                try:
                    escucha.notificar(evento)
                except Exception as e:
                    print(f"Error al notificar evento {tipo_evento.__name__}: {e}")
    
    def limpiar(self) -> None:
        """Limpia todos los escuchas registrados."""
        self._escuchas.clear()


# Mantener compatibilidad con código anterior
EventoPowerUpAgarrado = EventoPotenciadorRecogido
AdministradorDeEventos = AdministradorEventos
