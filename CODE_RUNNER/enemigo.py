from personaje import Personaje

class Enemigo(Personaje):
    """
    Clase para el enemigo que persigue al jugador en el laberinto.
    """
    def __init__(self, posicion, incremento_de_velocidad, deteccion, validador_posicion=None):
        super().__init__(posicion, validador_posicion)
        self.incremento_de_velocidad = incremento_de_velocidad  # int, pasos extra por turno
        self.deteccion = deteccion  # bool, si puede detectar al jugador

    def seguir_jugador(self, posicion_jugador):
        """
        Mueve al enemigo hacia la posición del jugador, considerando incremento de velocidad.
        """
        dx = posicion_jugador[0] - self.posicion[0]
        dy = posicion_jugador[1] - self.posicion[1]
        pasos = 1 + self.incremento_de_velocidad  # velocidad relativa
        nueva_x = self.posicion[0] + (pasos if dx > 0 else -pasos if dx < 0 else 0)
        nueva_y = self.posicion[1] + (pasos if dy > 0 else -pasos if dy < 0 else 0)
        # Solo mueve en una dirección por turno (prioridad eje x)
        if dx != 0:
            destino = (self.posicion[0] + (pasos if dx > 0 else -pasos), self.posicion[1])
        elif dy != 0:
            destino = (self.posicion[0], self.posicion[1] + (pasos if dy > 0 else -pasos))
        else:
            destino = self.posicion
        self.mover(destino)

    def detectar_jugador(self, posicion_jugador, rango_deteccion):
        """
        Devuelve True si el jugador está dentro del rango de detección.
        """
        dx = abs(posicion_jugador[0] - self.posicion[0])
        dy = abs(posicion_jugador[1] - self.posicion[1])
        return dx <= rango_deteccion and dy <= rango_deteccion

    def jugador_atrapado(self, posicion_jugador):
        """
        Devuelve True si el enemigo está en la misma posición que el jugador.
        """
        return self.posicion == posicion_jugador

