from personaje import Personaje
from pathfinding import bfs_siguiente_paso


class Enemigo(Personaje):
    """Clase para enemigos que persiguen al jugador"""

    def __init__(self, x: int, y: int, laberinto: list):
        super().__init__(x, y, nombre="Enemigo")
        self.laberinto = laberinto
        self.congelado = False
        self.duracion_congelamiento = 0

    def seguir_jugador(self, posicion_jugador: tuple) -> bool:
        """Intenta acercarse al jugador usando pathfinding"""
        if self.congelado:
            return False

        siguiente_pos = bfs_siguiente_paso(
            self.laberinto, self.obtener_posicion(), posicion_jugador
        )

        if siguiente_pos:
            return self.mover(siguiente_pos[0], siguiente_pos[1])
        return False

    def detectar_jugador(self, posicion_jugador: tuple, rango: int = 3) -> bool:
        """Detecta al jugador dentro de un rango"""
        dist_x = abs(self.posicion_x - posicion_jugador[0])
        dist_y = abs(self.posicion_y - posicion_jugador[1])
        return (dist_x + dist_y) <= rango

    def congelar(self, duracion: int):
        """Congela el enemigo por una duración"""
        self.congelado = True
        self.duracion_congelamiento = duracion

    def actualizar_congelamiento(self):
        """Actualiza el estado de congelamiento"""
        if self.duracion_congelamiento > 0:
            self.duracion_congelamiento -= 1
        else:
            self.congelado = False

    def obtener_estado(self) -> dict:
        """Retorna el estado del enemigo"""
        return {
            "posicion": self.obtener_posicion(),
            "congelado": self.congelado,
            "duracion_congelamiento": self.duracion_congelamiento,
        }
