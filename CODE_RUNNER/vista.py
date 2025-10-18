import pygame

class Vista:
    def __init__(self, ancho, alto, titulo=""):
        pygame.display.set_caption(titulo)
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
        self.fuente_hud = pygame.font.SysFont(None, 24)

    def limpiar_pantalla(self, color):
        self.pantalla.fill(color)

    def actualizar(self):
        pygame.display.flip()

    def dibujar_laberinto(self, laberinto, tam_celda):
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila):
                rect = pygame.Rect(x*tam_celda, y*tam_celda, tam_celda, tam_celda)
                color = (200, 200, 200) if celda == 1 else (50, 50, 50)
                pygame.draw.rect(self.pantalla, color, rect)

    def dibujar_jugador(self, x, y, tam):
        pygame.draw.circle(self.pantalla, (0, 0, 255), (x + tam//2, y + tam//2), tam//2)

    def dibujar_enemigo(self, x, y, tam):
        pygame.draw.circle(self.pantalla, (255, 0, 0), (x + tam//2, y + tam//2), tam//2)

    def dibujar_estrella(self, x, y, tam):
        rect = pygame.Rect(x + tam*0.25, y + tam*0.25, tam*0.5, tam*0.5)
        pygame.draw.rect(self.pantalla, (255, 255, 0), rect)

    def dibujar_hud(self, vidas, puntos):
        vidas_text = self.fuente_hud.render(f"Vidas: {vidas}", True, (255, 0, 0))
        puntos_text = self.fuente_hud.render(f"Puntos: {puntos}", True, (255, 255, 255))
        self.pantalla.blit(vidas_text, (10, 10))
        self.pantalla.blit(puntos_text, (self.ancho - puntos_text.get_width() - 10, 10))

    def dibujar_powerup(self, x, y, tam):
        """
        Dibuja un power-up como un cuadrado amarillo en el centro de la celda.
        """
        size = tam * 0.5
        offset = (tam - size) / 2
        rect = pygame.Rect(x + offset, y + offset, size, size)
        pygame.draw.rect(self.pantalla, (255, 255, 0), rect)

    def dibujar_texto(self, texto, x, y, tam_fuente, color):
        fuente = pygame.font.SysFont(None, tam_fuente)
        surf = fuente.render(texto, True, color)
        self.pantalla.blit(surf, (x, y))