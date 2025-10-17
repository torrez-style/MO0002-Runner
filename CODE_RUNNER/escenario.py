class Escenario:
    """
    Representa el laberinto del juego, incluyendo muros, pasillos, punto de inicio y obsequios.
    """
    def __init__(self, muros, pasillos, punto_de_inicio):
        """
        Inicializa el escenario.
        :param muros: iterable de tuplas (x, y) para posiciones de muros.
        :param pasillos: iterable de tuplas (x, y) para posiciones de pasillos.
        :param punto_de_inicio: tupla (x, y) para la posición inicial del jugador.
        """
        if not all(isinstance(pos, tuple) and len(pos) == 2 for pos in muros):
            raise ValueError("Todos los muros deben ser tuplas (x, y).")
        if not all(isinstance(pos, tuple) and len(pos) == 2 for pos in pasillos):
            raise ValueError("Todos los pasillos deben ser tuplas (x, y).")
        if not (isinstance(punto_de_inicio, tuple) and len(punto_de_inicio) == 2):
            raise ValueError("El punto de inicio debe ser una tupla (x, y).")
        self._muros = set(muros)
        self._pasillos = set(pasillos)
        self._punto_de_inicio = punto_de_inicio
        self._obsequios = set()

    @property
    def muros(self):
        return self._muros

    @property
    def pasillos(self):
        return self._pasillos

    @property
    def punto_de_inicio(self):
        return self._punto_de_inicio

    @property
    def obsequios(self):
        return self._obsequios

    def colision_con_pared(self, posicion):
        """
        Retorna True si la posición choca con un muro, False si está libre.
        """
        return posicion in self._muros

    def eliminar_obsequio_recogido(self, posicion):
        """
        Elimina un obsequio en la posición dada si existe.
        """
        self._obsequios.discard(posicion)

    def creacion_de_nuevos_obsequios(self, nuevas_posiciones):
        """
        Agrega nuevas posiciones donde se colocan obsequios.
        :param nuevas_posiciones: iterable de tuplas (x, y).
        """
        for pos in nuevas_posiciones:
            if not (isinstance(pos, tuple) and len(pos) == 2):
                raise ValueError("Cada obsequio debe estar en una tupla (x, y).")
        self._obsequios.update(nuevas_posiciones)

    def es_posicion_valida(self, posicion):
        """
        Retorna True si la posición está en pasillos y no es muro.
        """
        return posicion in self._pasillos and posicion not in self._muros
