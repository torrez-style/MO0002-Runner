"""Módulo de gestión de eventos para el juego"""


class Evento:
    """Clase base para todos los eventos"""
    pass

class EventoSalir(Evento):
    """Evento cuando el usuario quiere salir del juego"""
    pass

class EventoMoverJugador(Evento):
    """Evento cuando el jugador se mueve"""
    def __init__(self, direccion):
        self.direccion = direccion

class EventoRecogerEstrella(Evento):
    """Evento cuando el jugador recoge una estrella"""
    def __init__(self, posicion):
        self.posicion = posicion

class EventoColisionEnemigo(Evento):
    """Evento cuando el jugador colisiona con un enemigo"""
    def __init__(self, posicion_jugador, posicion_enemigo):
        self.posicion_jugador = posicion_jugador
        self.posicion_enemigo = posicion_enemigo

class EventoSeleccionMenu(Evento):
    """Evento cuando el usuario selecciona una opción del menú"""
    def __init__(self, opcion):
        self.opcion = opcion

class EventoGameOver(Evento):
    """Evento cuando el jugador pierde todas sus vidas"""
    def __init__(self, puntuacion_final):
        self.puntuacion_final = puntuacion_final

class AdministradorDeEventos:
    """Gestor central de eventos del juego"""
    def __init__(self):
        self.escuchas = {}

    def registrar(self, tipo_evento, escucha):
        if tipo_evento not in self.escuchas:
            self.escuchas[tipo_evento] = []
        if escucha not in self.escuchas[tipo_evento]:
            self.escuchas[tipo_evento].append(escucha)

    def desregistrar(self, tipo_evento, escucha):
        if tipo_evento in self.escuchas and escucha in self.escuchas[tipo_evento]:
            self.escuchas[tipo_evento].remove(escucha)

    def publicar(self, evento):
        tipo = type(evento)
        if tipo in self.escuchas:
            for escucha in list(self.escuchas[tipo]):
                escucha.notificar(evento)
