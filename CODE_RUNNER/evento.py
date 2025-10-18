

class Evento:
    """Clase base para todos los eventos"""
    pass

class EventoSalir(Evento):
    """Evento cuando el usuario quiere salir del juego"""
    pass

class EventoMoverJugador(Evento):
    """Evento cuando el jugador se mueve"""
    def __init__(self, direccion):
        self.direccion = direccion  # 'arriba', 'abajo', 'izquierda', 'derecha'

class EventoRecogerEstrella(Evento):
    """Evento cuando el jugador recoge una estrella"""
    def __init__(self, posicion):
        self.posicion = posicion  # tupla (x, y) en celdas

class EventoColisionEnemigo(Evento):
    """Evento cuando el jugador colisiona con un enemigo"""
    def __init__(self, posicion_jugador, posicion_enemigo):
        self.posicion_jugador = posicion_jugador  # (x, y) en celdas
        self.posicion_enemigo = posicion_enemigo  # (x, y) en celdas

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
