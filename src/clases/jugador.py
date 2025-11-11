from .personaje import Personaje


class Jugador(Personaje):
    """
    Representa al jugador controlado por el usuario.
    """
    
    def __init__(self, nombre, vidas, puntos=0, direccion=(0, 0), posicion=(1, 1), validador_posicion=None):
        """
        Inicializa un jugador.
        
        Args:
            nombre: Nombre del jugador (string).
            vidas: Número de vidas iniciales (entero positivo).
            puntos: Puntos iniciales (entero no negativo, por defecto 0).
            direccion: Dirección de movimiento inicial (tupla x, y, por defecto (0, 0)).
            posicion: Posición inicial (tupla x, y, por defecto (1, 1)).
            validador_posicion: Función de validación de posiciones.
        """
        self._validar_parametros_iniciales(nombre, vidas, puntos, direccion)
        
        super().__init__(posicion, validador_posicion)
        self._nombre = nombre
        self._vidas = vidas
        self._puntos = puntos
        self._direccion = direccion

    @property
    def nombre(self):
        """Devuelve el nombre del jugador."""
        return self._nombre

    @property
    def vidas(self):
        """Devuelve las vidas restantes del jugador."""
        return self._vidas

    @property
    def puntos(self):
        """Devuelve los puntos actuales del jugador."""
        return self._puntos

    @property
    def direccion(self):
        """Devuelve la dirección de movimiento actual."""
        return self._direccion

    def sumar_puntos(self, puntos):
        """
        Incrementa los puntos actuales cuando el jugador recoge puntos.
        
        Args:
            puntos: Número de puntos a añadir (entero positivo).
        """
        if not isinstance(puntos, int) or puntos <= 0:
            raise ValueError("Los puntos deben ser un entero positivo.")
        
        self._puntos += puntos

    def obtener_resumen_partida(self):
        """
        Devuelve un resumen del estado actual del jugador.
        
        Returns:
            str: Cadena con información del jugador.
        """
        return f"Jugador: {self._nombre}, Vidas: {self._vidas}, Puntos: {self._puntos}"

    def perder_vida(self):
        """
        Reduce en uno la cantidad de vidas.
        
        Returns:
            bool: True si el jugador perdió la última vida, False en caso contrario.
        """
        if self._vidas > 0:
            self._vidas -= 1
            return self._vidas == 0  # True si perdió la última vida
        return False

    def cambiar_direccion(self, nueva_direccion):
        """
        Cambia la dirección de movimiento del jugador.
        
        Args:
            nueva_direccion: Tupla (x, y) con la nueva dirección.
        """
        if not self._es_direccion_valida(nueva_direccion):
            raise ValueError("La nueva dirección debe ser una tupla de dos enteros (x, y).")
        
        self._direccion = nueva_direccion
    
    def _validar_parametros_iniciales(self, nombre, vidas, puntos, direccion):
        """Valida los parámetros iniciales del jugador."""
        if not isinstance(nombre, str):
            raise ValueError("El nombre debe ser un string.")
        
        if not isinstance(vidas, int) or vidas <= 0:
            raise ValueError("Las vidas deben ser un entero positivo.")
        
        if not isinstance(puntos, int) or puntos < 0:
            raise ValueError("Los puntos deben ser un entero no negativo.")
        
        if not self._es_direccion_valida(direccion):
            raise ValueError("La dirección debe ser una tupla de dos enteros (x, y).")
    
    def _es_direccion_valida(self, direccion):
        """Valida que la dirección sea una tupla de dos enteros."""
        return (isinstance(direccion, tuple) and 
                len(direccion) == 2 and 
                all(isinstance(coord, int) for coord in direccion))
