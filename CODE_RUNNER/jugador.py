from personaje import Personaje

class Jugador(Personaje):
    def __init__(self, nombre,vidas_restantes,puntos_actuales,direccion_de_movimiento,posicion, validador_posicion=None):
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser un string.")
        if not (isinstance(vidas_restantes, int) and vidas_restantes > 0):
            raise ValueError("Las vidas deben ser un entero positivo.")
        if not (isinstance(puntos_actuales, int) and puntos_actuales >= 0):
            raise ValueError("Los puntos deben ser un entero no negativo.")
        if not (isinstance(direccion_de_movimiento, tuple) and len(direccion_de_movimiento) == 2 and all(isinstance(coord, int) for coord in direccion_de_movimiento)):
            raise ValueError("La dirección debe ser una tupla de dos enteros (x, y).")
        super().__init__(posicion, validador_posicion)
        self._nombre=nombre
        self._vidas_restantes=vidas_restantes
        self._puntos_actuales=puntos_actuales
        self._direccion_de_movimiento=direccion_de_movimiento

    @property
    def nombre(self):
        return self._nombre

    @property
    def vidas_restantes(self):
        return self._vidas_restantes

    @property
    def puntos_actuales(self):
        return self._puntos_actuales

    @property
    def direccion_de_movimiento(self):
        return self._direccion_de_movimiento

    def recoger_puntos(self, puntos):
        #Incrementa los puntos actuales cuando el jugador recoge puntos en el juego.
        if not (isinstance(puntos, int) and puntos>0):
            raise ValueError("Los puntos deben ser un entero positivo.")
        self._puntos_actuales += puntos

    def mostrar_info_de_la_partida(self):
        #muestra un resumen del estado actual del jugador.
        return f"Jugador:{self._nombre}, Vidas: {self._vidas_restantes}, Puntos: {self._puntos_actuales}"

    def perdida_de_vida(self):
        #Reduce en uno la cantidad de vidas y devuelve True si el jugador pierde la última vida.
        if self._vidas_restantes > 0:
            self._vidas_restantes -= 1
            return self._vidas_restantes == 0  # True si perdió la última vida
        return False

    def cambiar_direccion(self, nueva_direccion):
        #Cambia la dirección de movimiento del jugador.
        if not (isinstance(nueva_direccion, tuple) and len(nueva_direccion) == 2 and all(isinstance(coord, int) for coord in nueva_direccion)):
            raise ValueError("La nueva dirección debe ser una tupla de dos enteros (x, y).")
        self._direccion_de_movimiento = nueva_direccion
