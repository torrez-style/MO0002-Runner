import pygame

class Vista:
    def __init__(self, ancho, alto, titulo=""):
        pygame.display.set_caption(titulo)
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
        self.fuente_hud = pygame.font.SysFont(None, 32)
        # offsets para centrar el laberinto dentro de un marco
        self.offset_x = 160  # margen izquierdo como en capturas
        self.offset_y = 90   # margen superior

    def limpiar_pantalla(self, color):
        self.pantalla.fill(color)

    def actualizar(self):
        pygame.display.flip()

    def dibujar_laberinto(self, laberinto, tam_celda, color_pared=(80,80,80), color_suelo=(220,220,220), dibujar_rejilla=True):
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila):
                rx = self.offset_x + x*tam_celda
                ry = self.offset_y + y*tam_celda
                rect = pygame.Rect(rx, ry, tam_celda, tam_celda)
                color = color_pared if celda == 1 else color_suelo
                pygame.draw.rect(self.pantalla, color, rect)
                if dibujar_rejilla:
                    pygame.draw.rect(self.pantalla, (40,40,40), rect, 1)

    def dibujar_jugador(self, x, y, tam):
        pygame.draw.circle(self.pantalla, (100, 0, 255), (self.offset_x + x + tam//2, self.offset_y + y + tam//2), tam//2)

    def dibujar_enemigo(self, x, y, tam):
        pygame.draw.circle(self.pantalla, (220, 50, 50), (self.offset_x + x + tam//2, self.offset_y + y + tam//2), tam//2)

    def dibujar_estrella(self, x, y, tam):
        rect = pygame.Rect(self.offset_x + x + tam*0.25, self.offset_y + y + tam*0.25, tam*0.5, tam*0.5)
        pygame.draw.rect(self.pantalla, (255, 215, 0), rect)

    def dibujar_hud(self, vidas, puntos):
        vidas_text = self.fuente_hud.render(f"Vidas: {vidas}", True, (255, 255, 255))
        puntos_text = self.fuente_hud.render(f"Puntos:  {puntos}", True, (255, 255, 255))
        self.pantalla.blit(vidas_text, (30, 24))
        self.pantalla.blit(puntos_text, (self.ancho - puntos_text.get_width() - 30, 24))

    def dibujar_powerup(self, x, y, tam):
        size = tam * 0.5
        offset = (tam - size) / 2
        rect = pygame.Rect(self.offset_x + x + offset, self.offset_y + y + offset, size, size)
        pygame.draw.rect(self.pantalla, (255, 255, 0), rect)

    def dibujar_texto(self, texto, x, y, tam_fuente, color=(255,255,255)):
        fuente = pygame.font.SysFont(None, tam_fuente)
        surf = fuente.render(texto, True, color)
        self.pantalla.blit(surf, (x, y))
