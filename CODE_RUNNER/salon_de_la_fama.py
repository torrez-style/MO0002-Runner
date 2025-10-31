class SalonDeLaFama:
    """
    Gestiona el ranking de los mejores puntajes del juego.
    """

    def __init__(self):
        # Lista de tuplas (nombre, puntaje)
        self._ranking = []

    @property
    def ranking(self):
        return list(self._ranking)

    def agregar_partida(self, nombre, puntaje):
        """
        Añade una nueva partida al ranking.
        """
        if not (isinstance(nombre, str) and isinstance(puntaje, int) and puntaje >= 0):
            raise ValueError("Nombre debe ser string y puntaje un entero no negativo.")
        self._ranking.append((nombre, puntaje))

    def _ordenar(self):
        self._ranking.sort(key=lambda x: x[1], reverse=True)

    def obtener_ranking(self, limite=10):
        """
        Devuelve el ranking ordenado como lista de tuplas (hasta 'limite').
        """
        self._ordenar()
        return self._ranking[:limite]
