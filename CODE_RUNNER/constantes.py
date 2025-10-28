"""
Constantes del juego Maze-Run.
Define colores, configuraciones y valores que se usan en todo el juego.
"""

# Colores principales del juego (RGB)
COLOR_JUGADOR = (100, 0, 255)  # Morado
COLOR_ENEMIGO = (220, 50, 50)  # Rojo
COLOR_ESTRELLA = (255, 255, 0)  # Amarillo
COLOR_POTENCIADOR = (0, 255, 0)  # Verde
COLOR_PARED_DEFAULT = (80, 80, 80)  # Gris oscuro
COLOR_SUELO_DEFAULT = (220, 230, 245)  # Azul claro
COLOR_FONDO = (0, 0, 0)  # Negro
COLOR_TEXTO = (255, 255, 255)  # Blanco
COLOR_TEXTO_DESTACADO = (255, 255, 0)  # Amarillo

# Configuración de pantalla
ANCHO_PANTALLA_DEFAULT = 900
ALTO_PANTALLA_DEFAULT = 700
FPS_DEFAULT = 50

# Configuración de juego
TAMAÑO_CELDA = 32
VIDAS_INICIALES = 3
PUNTOS_POR_ESTRELLA = 10
DURACION_POTENCIADOR = 300  # frames
VELOCIDAD_ENEMIGOS_DEFAULT = 14
RETRASO_MOVIMIENTO_JUGADOR = 7

# Tipos de celdas en el laberinto
CELDA_VACIA = 0
CELDA_PARED = 1
CELDA_ENTRADA = 2
CELDA_SALIDA = 3

# Tipos de potenciadores
POTENCIADOR_INVULNERABLE = 'invulnerable'
POTENCIADOR_CONGELAR = 'congelar'
POTENCIADOR_INVISIBLE = 'invisible'

# Direcciones de movimiento
DIRECCION_ARRIBA = (0, -1)
DIRECCION_ABAJO = (0, 1)
DIRECCION_IZQUIERDA = (-1, 0)
DIRECCION_DERECHA = (1, 0)
DIRECCION_QUIETO = (0, 0)
