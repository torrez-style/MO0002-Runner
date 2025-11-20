class Personaje:
    def __init__(self, posicion, validador_posicion=None):
        if not (isinstance(posicion, tuple) and len(posicion) == 2 and
                all(isinstance(coord, int) for coord in posicion)):
            raise ValueError("La posición debe ser una tupla de dos enteros (x, y).")
        self._posicion = posicion
        self._validador_posicion = validador_posicion

    @property
    def posicion(self):
        #Devuelve la posición actual del personaje.
        return self._posicion
    def mover(self, nueva_posicion):
        if not (isinstance(nueva_posicion, tuple) and len(nueva_posicion) == 2 and
                all(isinstance(coord, int) for coord in nueva_posicion)):
            raise ValueError("La nueva posición debe ser una tupla de dos enteros (x, y).")
        if self._validador_posicion:
            if not self._validador_posicion(nueva_posicion):
                print("Movimiento bloqueado: posición inválida (muro o fuera de límites).")
                return False
        self._posicion = nueva_posicion
        return True
