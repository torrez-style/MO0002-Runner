class Puntuacion:
    """
    Gestiona la puntuación y los obsequios recogidos por el jugador.
    """

    def __init__(self, puntos=0, obsequios=0):
        if not (isinstance(puntos, int) and puntos >= 0):
            raise ValueError("Los puntos deben ser un entero no negativo.")
        if not (isinstance(obsequios, int) and obsequios >= 0):
            raise ValueError("Los obsequios deben ser un entero no negativo.")
        self._puntos = puntos
        self._obsequios = obsequios

    @property
    def puntos(self):
        return self._puntos

    @property
    def obsequios(self):
        return self._obsequios

    @property
    def total(self):
        """Puntos totales calculados on the fly para evitar desincronización."""
        return self._puntos + self._obsequios

    def sumar_puntos(self, cantidad):
        """
        Suma puntos a la puntuación actual.
        """
        if not (isinstance(cantidad, int) and cantidad >= 0):
            raise ValueError("La cantidad de puntos debe ser un entero no negativo.")
        self._puntos += cantidad

    def sumar_obsequios(self, cantidad):
        """
        Suma obsequios a la puntuación actual.
        """
        if not (isinstance(cantidad, int) and cantidad >= 0):
            raise ValueError("La cantidad de obsequios debe ser un entero no negativo.")
        self._obsequios += cantidad
