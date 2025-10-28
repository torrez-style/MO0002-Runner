"""
Módulo de algoritmos de búsqueda de caminos para el juego Maze-Run.
Implementa BFS para encontrar rutas óptimas en el laberinto.
"""

from collections import deque
from typing import List, Tuple, Optional, Set


def encontrar_siguiente_paso_bfs(laberinto: List[List[int]], inicio: Tuple[int, int], 
                                  objetivo: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """
    Encuentra el siguiente paso en el camino más corto usando BFS.
    
    Args:
        laberinto: Matriz 2D donde 0=camino libre, 1=pared.
        inicio: Posición actual (x, y) del enemigo.
        objetivo: Posición (x, y) del jugador.
    
    Returns:
        Tupla (x, y) del siguiente paso, o None si no hay camino.
    
    Raises:
        ValueError: Si los parámetros son inválidos.
    """
    if not _validar_parametros_pathfinding(laberinto, inicio, objetivo):
        return None
    
    if inicio == objetivo:
        return inicio
    
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    # Cola para BFS: (posición, camino)
    cola = deque([(inicio, [inicio])])
    visitados: Set[Tuple[int, int]] = {inicio}
    
    # Direcciones: arriba, abajo, izquierda, derecha
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    while cola:
        (x, y), camino = cola.popleft()
        
        # Explorar vecinos
        for delta_x, delta_y in direcciones:
            nueva_x, nueva_y = x + delta_x, y + delta_y
            
            # Verificar límites y que sea camino libre
            if _es_posicion_valida(nueva_x, nueva_y, columnas, filas, laberinto):
                if (nueva_x, nueva_y) not in visitados:
                    visitados.add((nueva_x, nueva_y))
                    camino_nuevo = camino + [(nueva_x, nueva_y)]
                    
                    # Si llegamos al objetivo, devolver el siguiente paso
                    if (nueva_x, nueva_y) == objetivo:
                        return camino_nuevo[1] if len(camino_nuevo) > 1 else inicio
                    
                    cola.append(((nueva_x, nueva_y), camino_nuevo))
    
    # No hay camino disponible
    return None


def calcular_distancia_manhattan(posicion1: Tuple[int, int], posicion2: Tuple[int, int]) -> int:
    """
    Calcula la distancia Manhattan entre dos posiciones.
    
    Args:
        posicion1: Primera posición (x, y).
        posicion2: Segunda posición (x, y).
    
    Returns:
        Distancia Manhattan como entero.
    """
    return abs(posicion1[0] - posicion2[0]) + abs(posicion1[1] - posicion2[1])


def calcular_distancia_euclidiana(posicion1: Tuple[int, int], posicion2: Tuple[int, int]) -> float:
    """
    Calcula la distancia euclidiana entre dos posiciones.
    
    Args:
        posicion1: Primera posición (x, y).
        posicion2: Segunda posición (x, y).
    
    Returns:
        Distancia euclidiana como float.
    """
    return ((posicion1[0] - posicion2[0]) ** 2 + (posicion1[1] - posicion2[1]) ** 2) ** 0.5


def obtener_posiciones_adyacentes(posicion: Tuple[int, int], laberinto: List[List[int]]) -> List[Tuple[int, int]]:
    """
    Obtiene todas las posiciones adyacentes válidas (no son paredes) de una posición dada.
    
    Args:
        posicion: Posición actual (x, y).
        laberinto: Matriz del laberinto.
    
    Returns:
        Lista de posiciones adyacentes válidas.
    """
    if not laberinto or not laberinto[0]:
        return []
    
    x, y = posicion
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    posiciones_validas = []
    
    for delta_x, delta_y in direcciones:
        nueva_x, nueva_y = x + delta_x, y + delta_y
        
        if _es_posicion_valida(nueva_x, nueva_y, columnas, filas, laberinto):
            posiciones_validas.append((nueva_x, nueva_y))
    
    return posiciones_validas


def _validar_parametros_pathfinding(laberinto: List[List[int]], inicio: Tuple[int, int], 
                                     objetivo: Tuple[int, int]) -> bool:
    """
    Valida que los parámetros para pathfinding sean correctos.
    
    Args:
        laberinto: Matriz del laberinto a validar.
        inicio: Posición de inicio a validar.
        objetivo: Posición objetivo a validar.
    
    Returns:
        True si los parámetros son válidos, False en caso contrario.
    """
    if not laberinto or not laberinto[0]:
        return False
    
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    # Validar que las posiciones estén dentro de los límites
    if not (0 <= inicio[0] < columnas and 0 <= inicio[1] < filas):
        return False
        
    if not (0 <= objetivo[0] < columnas and 0 <= objetivo[1] < filas):
        return False
    
    # Validar que las posiciones no sean paredes
    if laberinto[inicio[1]][inicio[0]] == 1 or laberinto[objetivo[1]][objetivo[0]] == 1:
        return False
    
    return True


def _es_posicion_valida(x: int, y: int, columnas: int, filas: int, laberinto: List[List[int]]) -> bool:
    """
    Verifica si una posición está dentro de los límites y es un camino libre.
    
    Args:
        x: Coordenada x.
        y: Coordenada y.
        columnas: Número total de columnas.
        filas: Número total de filas.
        laberinto: Matriz del laberinto.
    
    Returns:
        True si la posición es válida, False en caso contrario.
    """
    return (0 <= x < columnas and 
            0 <= y < filas and 
            laberinto[y][x] == 0)


# Mantener compatibilidad con código anterior
bfs_siguiente_paso = encontrar_siguiente_paso_bfs
