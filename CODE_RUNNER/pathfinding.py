# pathfinding.py
from collections import deque

def bfs_siguiente_paso(laberinto, inicio, objetivo):
    """
    Encuentra el siguiente paso en el camino más corto usando BFS.
    
    Args:
        laberinto: Matriz 2D (0=camino, 1=pared)
        inicio: Tupla (x, y) posición actual del enemigo
        objetivo: Tupla (x, y) posición del jugador
    
    Returns:
        Tupla (x, y) del siguiente paso, o None si no hay camino
    """
    if inicio == objetivo:
        return inicio
    
    filas = len(laberinto)
    columnas = len(laberinto[0])
    
    # Cola para BFS: (posición, camino)
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}
    
    # Direcciones: arriba, abajo, izquierda, derecha
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    while cola:
        (x, y), camino = cola.popleft()
        
        # Explorar vecinos
        for delta_x, delta_y in direcciones:
            nueva_x, nueva_y = x + delta_x, y + delta_y
            
            # Verificar límites y que sea camino
            if 0 <= nueva_x < columnas and 0 <= nueva_y < filas and laberinto[nueva_y][nueva_x] == 0:
                if (nueva_x, nueva_y) not in visitados:
                    visitados.add((nueva_x, nueva_y))
                    camino_nuevo = camino + [(nueva_x, nueva_y)]
                    
                    # Si llegamos al objetivo, devolver el siguiente paso
                    if (nueva_x, nueva_y) == objetivo:
                        return camino_nuevo[1] if len(camino_nuevo) > 1 else inicio
                    
                    cola.append(((nueva_x, nueva_y), camino_nuevo))
    
    # No hay camino disponible
    return None


def calcular_distancia_manhattan(posicion1, posicion2):
    """Calcula la distancia Manhattan entre dos posiciones"""
    return abs(posicion1[0] - posicion2[0]) + abs(posicion1[1] - posicion2[1])
