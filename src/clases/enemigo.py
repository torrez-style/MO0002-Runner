from .personaje import Personaje


class Enemigo(Personaje):
    """
    Clase para el enemigo que persigue al jugador en el laberinto.
    """
    
    def __init__(self, posicion, velocidad_extra=0, puede_detectar=True, validador_posicion=None):
        """
        Inicializa un enemigo.
        
        Args:
            posicion: Posición inicial del enemigo (tupla x, y).
            velocidad_extra: Pasos extra por turno (entero, por defecto 0).
            puede_detectar: Si puede detectar al jugador (bool, por defecto True).
            validador_posicion: Función de validación de posiciones.
        """
        super().__init__(posicion, validador_posicion)
        self.velocidad_extra = velocidad_extra
        self.puede_detectar = puede_detectar

    def perseguir_jugador(self, posicion_jugador):
        """
        Mueve al enemigo hacia la posición del jugador.
        
        Args:
            posicion_jugador: Posición actual del jugador (tupla x, y).
        """
        if not self.puede_detectar:
            return
        
        diferencia_x = posicion_jugador[0] - self.posicion[0]
        diferencia_y = posicion_jugador[1] - self.posicion[1]
        
        pasos = 1 + self.velocidad_extra
        
        # Calcular nueva posición priorizando movimiento en X
        if diferencia_x != 0:
            direccion_x = pasos if diferencia_x > 0 else -pasos
            nueva_posicion = (self.posicion[0] + direccion_x, self.posicion[1])
        elif diferencia_y != 0:
            direccion_y = pasos if diferencia_y > 0 else -pasos
            nueva_posicion = (self.posicion[0], self.posicion[1] + direccion_y)
        else:
            nueva_posicion = self.posicion
        
        self.mover(nueva_posicion)

    def esta_en_rango_deteccion(self, posicion_jugador, rango_deteccion):
        """
        Verifica si el jugador está dentro del rango de detección.
        
        Args:
            posicion_jugador: Posición del jugador (tupla x, y).
            rango_deteccion: Distancia máxima de detección (entero).
            
        Returns:
            bool: True si el jugador está en rango, False en caso contrario.
        """
        if not self.puede_detectar:
            return False
        
        distancia_x = abs(posicion_jugador[0] - self.posicion[0])
        distancia_y = abs(posicion_jugador[1] - self.posicion[1])
        
        return distancia_x <= rango_deteccion and distancia_y <= rango_deteccion

    def ha_atrapado_jugador(self, posicion_jugador):
        """
        Verifica si el enemigo está en la misma posición que el jugador.
        
        Args:
            posicion_jugador: Posición del jugador (tupla x, y).
            
        Returns:
            bool: True si están en la misma posición, False en caso contrario.
        """
        return self.posicion == posicion_jugador
