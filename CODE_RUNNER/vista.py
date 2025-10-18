
import pygame

class Vista:
    """
    Maneja todo el renderizado visual del juego.
    No contiene lógica de juego, solo dibuja en pantalla.
    """

    def __init__(self, ancho_pantalla, alto_pantalla, titulo="MAZE-RUN"):
        """
        Inicializa la ventana del juego.

        Args:
            ancho_pantalla: Ancho de la ventana en píxeles.
            alto_pantalla: Alto de la ventana en píxeles.
            titulo: Título de la ventana.
        """
        pygame.init()
        self.ancho_pantalla = ancho_pantalla
        self.alto_pantalla = alto_pantalla
        self.pantalla = pygame.display.set_mode((ancho_pantalla, alto_pantalla))
        pygame.display.set_caption(titulo)

        # Colores comunes (puedes moverlos luego a config.py)
        self.COLOR_NEGRO = (0, 0, 0)
        self.COLOR_BLANCO = (255, 255, 255)
        self.COLOR_VERDE = (0, 255, 0)
        self.COLOR_ROJO = (255, 0, 0)
        self.COLOR_AZUL = (0, 0, 255)
        self.COLOR_GRIS = (128, 128, 128)

    def limpiar_pantalla(self, color=None):
        """
        Limpia la pantalla con un color de fondo.

        Args:
            color: Tupla RGB del color de fondo. Si es None, usa negro.
        """
        if color is None:
            color = self.COLOR_NEGRO
        self.pantalla.fill(color)

    def dibujar_laberinto(self, laberinto, tamano_celda):
        """
        Dibuja la estructura del laberinto.

        Args:
            laberinto: Matriz 2D con el laberinto (0=camino, 1=pared).
            tamano_celda: Tamaño en píxeles de cada celda.
        """
        for fila in range(len(laberinto)):
            for col in range(len(laberinto[fila])):
                x = col * tamano_celda
                y = fila * tamano_celda

                if laberinto[fila][col] == 1:
                    color = self.COLOR_GRIS
                else:
                    color = self.COLOR_BLANCO

                pygame.draw.rect(self.pantalla, color, (x, y, tamano_celda, tamano_celda))
                # Borde de celda
                pygame.draw.rect(self.pantalla, self.COLOR_NEGRO, (x, y, tamano_celda, tamano_celda), 1)

    def dibujar_jugador(self, x, y, tamano):
        """
        Dibuja al jugador.

        Args:
            x: Posición X en píxeles.
            y: Posición Y en píxeles.
            tamano: Tamaño en píxeles.
        """
        pygame.draw.circle(
            self.pantalla,
            self.COLOR_AZUL,
            (x + tamano // 2, y + tamano // 2),
            tamano // 2
        )

    def dibujar_enemigo(self, x, y, tamano):
        """
        Dibuja un enemigo.

        Args:
            x: Posición X en píxeles.
            y: Posición Y en píxeles.
            tamano: Tamaño en píxeles.
        """
        pygame.draw.circle(
            self.pantalla,
            self.COLOR_ROJO,
            (x + tamano // 2, y + tamano // 2),
            tamano // 2
        )

    def dibujar_estrella(self, x, y, tamano):
        """
        Dibuja una estrella coleccionable.

        Args:
            x: Posición X en píxeles.
            y: Posición Y en píxeles.
            tamano: Tamaño en píxeles.
        """
        pygame.draw.rect(
            self.pantalla,
            (255, 255, 0),  # Amarillo
            (x + tamano // 4, y + tamano // 4, tamano // 2, tamano // 2)
        )

    def dibujar_texto(self, texto, x, y, tamano_fuente=24, color=None):
        """
        Dibuja texto en la pantalla.

        Args:
            texto: El texto a mostrar.
            x: Posición X en píxeles.
            y: Posición Y en píxeles.
            tamano_fuente: Tamaño de la fuente.
            color: Color del texto (tupla RGB). Si es None, blanco.
        """
        if color is None:
            color = self.COLOR_BLANCO
        fuente = pygame.font.Font(None, tamano_fuente)
        superficie = fuente.render(texto, True, color)
        self.pantalla.blit(superficie, (x, y))

    def dibujar_hud(self, vidas, puntos):
        """
        Dibuja el HUD con vidas y puntos.

        Args:
            vidas: Número de vidas.
            puntos: Puntuación actual.
        """
        # Vidas
        self.dibujar_texto(f"Vidas: {vidas}", 10, 10, tamano_fuente=32, color=self.COLOR_ROJO)
        # Puntos
        texto_puntos = f"Puntos: {puntos}"
        ancho_texto = len(texto_puntos) * 15
        self.dibujar_texto(texto_puntos, self.ancho_pantalla - ancho_texto - 10, 10, tamano_fuente=32)

    def actualizar(self):
        """
        Refresca la pantalla.
        """
        pygame.display.flip()
