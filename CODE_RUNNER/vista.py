import pygame
from constantes import (
    COLOR_JUGADOR, COLOR_ENEMIGO,
    COLOR_PARED_DEFAULT, COLOR_SUELO_DEFAULT,
)


# Estados del juego (evitar tildes en claves lógicas)
ESTADO_MENU = "MENU"
ESTADO_JUEGO = "JUEGO"
ESTADO_GAME_OVER = "GAME_OVER"
ESTADO_SALON = "SALON_DE_LA_FAMA"
ESTADO_ADMIN = "ADMINISTRACION"

class Vista:
    def __init__(self, ancho, alto, titulo=""):
        pygame.display.set_caption(titulo)
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
        self.fuente_interfaz = pygame.font.SysFont(None, 32)
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0

    def limpiar_pantalla(self, color):
        self.pantalla.fill(color)

    def actualizar(self):
        pygame.display.flip()

    def dibujar_laberinto(self, laberinto, tamano_celda, color_pared=COLOR_PARED_DEFAULT, color_suelo=COLOR_SUELO_DEFAULT, mostrar_rejilla=True):
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila):
                posicion_x = self.desplazamiento_x + x * tamano_celda
                posicion_y = self.desplazamiento_y + y * tamano_celda
                rectangulo = pygame.Rect(posicion_x, posicion_y, tamano_celda, tamano_celda)
                if celda == 1:
                    color = color_pared
                elif celda == 2:
                    color = (255, 150, 0)  # entrada
                elif celda == 3:
                    color = (0, 255, 0)  # salida
                else:
                    color = color_suelo
                pygame.draw.rect(self.pantalla, color, rectangulo)
                if mostrar_rejilla:
                    pygame.draw.rect(self.pantalla, (40, 40, 40), rectangulo, 1)

    def dibujar_jugador(self, x, y, tamano):
        pygame.draw.circle(
            self.pantalla, COLOR_JUGADOR,
            (self.desplazamiento_x + x + tamano // 2, self.desplazamiento_y + y + tamano // 2),
            tamano // 2,
        )

    def dibujar_enemigo(self, x, y, tamano, color=COLOR_ENEMIGO):
        pygame.draw.circle(
            self.pantalla, color,
            (self.desplazamiento_x + x + tamano // 2, self.desplazamiento_y + y + tamano // 2),
            tamano // 2,
        )

    def dibujar_estrella(self, x, y, tamano):
        rectangulo = pygame.Rect(
            self.desplazamiento_x + x + tamano * 0.25,
            self.desplazamiento_y + y + tamano * 0.25,
            tamano * 0.5,
            tamano * 0.5,
        )
        pygame.draw.rect(self.pantalla, (255, 215, 0), rectangulo)

    def dibujar_interfaz(self, vidas, puntos, x=30, y=24):
        texto_vidas = self.fuente_interfaz.render(f"Vidas: {vidas}", True, (255, 255, 255))
        texto_puntos = self.fuente_interfaz.render(f"Puntos:  {puntos}", True, (255, 255, 255))
        self.pantalla.blit(texto_vidas, (x, y))
        self.pantalla.blit(texto_puntos, (self.ancho - texto_puntos.get_width() - 30, y))

    def dibujar_potenciador(self, x, y, tamano):
        dimension = tamano * 0.5
        desplazamiento = (tamano - dimension) / 2
        rectangulo = pygame.Rect(
            self.desplazamiento_x + x + desplazamiento,
            self.desplazamiento_y + y + desplazamiento,
            dimension,
            dimension,
        )
        pygame.draw.rect(self.pantalla, (255, 255, 0), rectangulo)

    def dibujar_texto(self, texto, x, y, tamano_fuente, color=(255, 255, 255)):
        fuente = pygame.font.SysFont(None, tamano_fuente)
        superficie = fuente.render(texto, True, color)
        self.pantalla.blit(superficie, (x, y))
