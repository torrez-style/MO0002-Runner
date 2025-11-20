class Personaje:
    """Clase base para todos los personajes del juego"""

    def __init__(self, x: int, y: int, nombre: str = "Personaje"):
        self.posicion_x = x
        self.posicion_y = y
        self.nombre = nombre

    def mover(self, nueva_x: int, nueva_y: int) -> bool:
        """Intenta mover el personaje a una nueva posición"""
        if self._validar_posicion(nueva_x, nueva_y):
            self.posicion_x = nueva_x
            self.posicion_y = nueva_y
            return True
        return False

    def _validar_posicion(self, x: int, y: int) -> bool:
        """Valida que la posición sea válida"""
        return isinstance(x, int) and isinstance(y, int) and x >= 0 and y >= 0

    def obtener_posicion(self) -> tuple:
        """Retorna la posición actual del personaje"""
        return (self.posicion_x, self.posicion_y)

    def __repr__(self) -> str:
        return f"{self.nombre} en ({self.posicion_x}, {self.posicion_y})"
