class SalondelaFama:
    """
    Gestiona el ranking de los mejores puntajes del juego.
    """
    def __init__(self):
        self._lista_de_jugadores = []  # Lista de tuplas (nombre, puntaje)

    @property
    def lista_de_jugadores(self):
        return self._lista_de_jugadores

    def agregar_partida(self, nombre, puntaje):
        """
        Añade una nueva partida al ranking.
        """
        if not (isinstance(nombre, str) and isinstance(puntaje, int) and puntaje >= 0):
            raise ValueError("Nombre debe ser string y puntaje un entero no negativo.")
        self._lista_de_jugadores.append((nombre, puntaje))

    def ordenar_ranking(self):
        """
        Ordena la lista de jugadores de mayor a menor puntaje.
        """
        self._lista_de_jugadores.sort(key=lambda x: x[1], reverse=True)

    def mostrar_ranking(self):
        """
        Muestra el ranking ordenado.
        """
        self.ordenar_ranking()
        print("Ranking Salón de la Fama")
        for idx, (nombre, puntaje) in enumerate(self._lista_de_jugadores, 1):
            print(f"{idx}. {nombre} - {puntaje}")

    def obtener_ranking(self):
        """
        Devuelve el ranking ordenado como lista de tuplas.
        """
        self.ordenar_ranking()
        return list(self._lista_de_jugadores)
