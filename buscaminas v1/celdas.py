
# celda.py
class Celdas:
    """Representa una celda individual en el tablero."""

    def __init__(self):
        self._es_mina = False  # ¿Tiene una mina?
        self._esta_revelada = False  # ¿Ha sido abierta por el jugador?
        self._mina_vecina_contador = 0  # Número de minas en celdas adyacentes

    def colocar_mina(self):
        """Marca esta celda como una mina."""
        self._es_mina = True

    def es_mina(self):
        """Retorna True si la celda es una mina."""
        return self._es_mina

    def revelar(self):
        """Marca la celda como revelada."""
        self._esta_revelada = True

    def esta_revelada(self):
        """Retorna True si la celda ya fue revelada."""
        return self._esta_revelada

    def incrementar_contador(self):
        """Aumenta el contador de minas vecinas."""
        self._mina_vecina_contador += 1

    def obtener_valor_a_mostrar(self):
        """Retorna el carácter que debe mostrarse en la terminal."""
        if not self._esta_revelada:
            # Oculto
            return '#'
        elif self._es_mina:
            # Revelado y es una mina
            return '*'
        elif self._mina_vecina_contador > 0:
            # Revelado y tiene minas vecinas
            return str(self._mina_vecina_contador)
        else:
            # Revelado y no tiene minas vecinas (es un espacio en blanco)
            return ' '


