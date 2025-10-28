"""Módulo de gestión de eventos para el juego"""

# evento.py

class Evento:
    pass

class EventoSalir(Evento):
    pass

class EventoMoverJugador(Evento):
    def __init__(self, direccion):
        self.direccion = direccion

class EventoRecogerEstrella(Evento):
    def __init__(self, posicion):
        self.posicion = posicion

class EventoColisionEnemigo(Evento):
    def __init__(self, posicion_jugador, posicion_enemigo):
        self.posicion_jugador = posicion_jugador
        self.posicion_enemigo = posicion_enemigo

class EventoSeleccionMenu(Evento):
    def __init__(self, opcion):
        self.opcion = opcion

class EventoFinDeJuego(Evento):
    def __init__(self, puntuacion_final):
        self.puntuacion_final = puntuacion_final

class EventoPowerUpAgarrado(Evento):
    def __init__(self, tipo):
        self.tipo = tipo  # 'invulnerable', 'congelar', 'invisible'

class EventoSalirNivel(Evento):
    """Evento que se dispara cuando el jugador llega a la salida del nivel"""
    pass

class AdministradorDeEventos:
    def __init__(self):
        self.escuchas = {}

    def registrar(self, tipo_evento, escucha):
        if tipo_evento not in self.escuchas:
            self.escuchas[tipo_evento] = []
        if escucha not in self.escuchas[tipo_evento]:
            self.escuchas[tipo_evento].append(escucha)

    def publicar(self, evento):
        tipo = type(evento)
        if tipo in self.escuchas:
            for escucha in list(self.escuchas[tipo]):
                escucha.notificar(evento)