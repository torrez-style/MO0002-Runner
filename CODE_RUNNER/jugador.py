from personaje import Personaje


class Jugador(Personaje):
    """Clase para el jugador controlable"""

    def __init__(self, x: int, y: int, nombre_usuario: str, vidas: int = 3):
        super().__init__(x, y, nombre="Jugador")
        self.nombre_usuario = nombre_usuario
        self.vidas = vidas
        self.puntos = 0
        self.invulnerable = False
        self.invisible = False
        self.duracion_powerup = 0

    def recoger_puntos(self, cantidad: int):
        """Suma puntos al jugador"""
        if cantidad > 0:
            self.puntos += cantidad

    def perder_vida(self) -> bool:
        """El jugador pierde una vida. Retorna True si aún tiene vidas"""
        if not self.invulnerable:
            self.vidas -= 1
            return self.vidas > 0
        return True

    def activar_powerup(self, tipo_powerup: str, duracion: int):
        """Activa un powerup temporal"""
        if tipo_powerup == "invulnerable":
            self.invulnerable = True
        elif tipo_powerup == "invisible":
            self.invisible = True
        self.duracion_powerup = duracion

    def desactivar_powerup(self):
        """Desactiva los powerups activos"""
        self.invulnerable = False
        self.invisible = False
        self.duracion_powerup = 0

    def actualizar_powerup(self):
        """Actualiza la duración del powerup"""
        if self.duracion_powerup > 0:
            self.duracion_powerup -= 1
        else:
            self.desactivar_powerup()

    def obtener_estado(self) -> dict:
        """Retorna el estado completo del jugador"""
        return {
            "nombre_usuario": self.nombre_usuario,
            "posicion": self.obtener_posicion(),
            "vidas": self.vidas,
            "puntos": self.puntos,
            "invulnerable": self.invulnerable,
            "invisible": self.invisible,
        }
