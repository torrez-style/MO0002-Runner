class Puntuacion:
    def __init__(self, puntos=0, obsequios=0):
        if not (isinstance(puntos, int) and puntos >= 0):
            raise ValueError("Los puntos deben ser un entero no negativo.")
        if not (isinstance(obsequios, int) and obsequios >= 0):
            raise ValueError("Los obsequios deben ser un entero no negativo.")
        self._puntos = puntos
        self._obsequios = obsequios
        self._total_de_puntos = puntos + obsequios
    @property
    def puntos(self):
        return self._puntos
    @property
    def obsequios(self):
        return self._obsequios
    @property
    def total_de_puntos(self):
        return self._total_de_puntos
    def agregar_puntos(self, cantidad):
        #Suma puntos a la puntuación actual y actualiza el total.
        if not (isinstance(cantidad, int) and cantidad >= 0):
            raise ValueError("La cantidad de puntos debe ser un entero no negativo.")
        self._puntos += cantidad
        self.contador_total()
    def agregar_obsequios(self, cantidad):
        #Suma obsequios a la puntuación actual y actualiza el total.
        if not (isinstance(cantidad, int) and cantidad >= 0):
            raise ValueError("La cantidad de obsequios debe ser un entero no negativo.")
        self._obsequios += cantidad
        self.contador_total()
    def contador_total(self):
        #Actualiza el total de puntos.
        self._total_de_puntos = self._puntos + self._obsequios
