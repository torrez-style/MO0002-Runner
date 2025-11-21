def bfs_siguiente_paso(laberinto, posicion_actual, destino):
    """
    Encuentra el siguiente paso hacia el destino usando BFS.
    Retorna la posición del siguiente paso.
    """
    from collections import deque

    if posicion_actual == destino:
        return posicion_actual

    filas, cols = len(laberinto), len(laberinto[0])
    visitados = set()
    cola = deque([(posicion_actual, [posicion_actual])])
    visitados.add(posicion_actual)

    while cola:
        (x, y), camino = cola.popleft()

        # Explora las 4 direcciones
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy

            if (
                0 <= nx < filas
                and 0 <= ny < cols
                and (nx, ny) not in visitados
                and laberinto[nx][ny] != 1
            ):
                if (nx, ny) == destino:
                    return (nx, ny)

                visitados.add((nx, ny))
                cola.append(((nx, ny), camino + [(nx, ny)]))

    return posicion_actual
