class Personaje:
    """
    Clase base para cualquier personaje del juego (jugador o enemigo).
    Gestiona la posición y el movimiento básico, con validaciones.
    """
    
    def __init__(self, posicion, validador_posicion=None):
        """
        Inicializa el personaje en una posición dada.
        
        Args:
            posicion: Tupla (x, y) con coordenadas iniciales.
            validador_posicion: Función que valida si una posición es válida.
        """
        if not self._es_posicion_valida(posicion):
            raise ValueError("La posición debe ser una tupla de dos enteros (x, y).")
        
        self._posicion = posicion
        self._validador_posicion = validador_posicion

    @property
    def posicion(self):
        """Devuelve la posición actual del personaje."""
        return self._posicion

    def mover(self, nueva_posicion):
        """
        Intenta mover al personaje a una nueva posición.
        
        Args:
            nueva_posicion: Tupla (x, y) con la nueva posición.
            
        Returns:
            bool: True si el movimiento fue exitoso, False si no.
        """
        if not self._es_posicion_valida(nueva_posicion):
            raise ValueError("La nueva posición debe ser una tupla de dos enteros (x, y).")
        
        if self._validador_posicion and not self._validador_posicion(nueva_posicion):
            print("Movimiento bloqueado: posición inválida (muro o fuera de límites).")
            return False
        
        self._posicion = nueva_posicion
        return True
    
    def _es_posicion_valida(self, posicion):
        """Valida que la posición sea una tupla de dos enteros."""
        return (isinstance(posicion, tuple) and 
                len(posicion) == 2 and
                all(isinstance(coord, int) for coord in posicion))
