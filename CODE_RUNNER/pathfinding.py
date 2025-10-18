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
    cols = len(laberinto[0])
    
    # Cola para BFS: (posición, camino)
    cola = deque([(inicio, [inicio])])
    visitados = {inicio}
    
    # Direcciones: arriba, abajo, izquierda, derecha
    direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    while cola:
        (x, y), camino = cola.popleft()
        
        # Explorar vecinos
        for dx, dy in direcciones:
            nx, ny = x + dx, y + dy
            
            # Verificar límites y que sea camino
            if 0 <= nx < cols and 0 <= ny < filas and laberinto[ny][nx] == 0:
                if (nx, ny) not in visitados:
                    visitados.add((nx, ny))
                    nuevo_camino = camino + [(nx, ny)]
                    
                    # Si llegamos al objetivo, devolver el siguiente paso
                    if (nx, ny) == objetivo:
                        return nuevo_camino[1] if len(nuevo_camino) > 1 else inicio
                    
                    cola.append(((nx, ny), nuevo_camino))
    
    # No hay camino disponible
    return None


def distancia_manhattan(pos1, pos2):
    """Calcula la distancia Manhattan entre dos posiciones"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
