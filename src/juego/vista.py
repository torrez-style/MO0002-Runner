import pygame
from .constantes import (
    COLOR_JUGADOR, COLOR_ENEMIGO,
    COLOR_PARED_DEFAULT, COLOR_SUELO_DEFAULT,
)


class Vista:
    def __init__(self, ancho, alto, titulo=""):
        pygame.display.set_caption(titulo)
        self.pantalla = pygame.display.set_mode((ancho, alto))
        self.ancho = ancho
        self.alto = alto
        self.fuente_interfaz = pygame.font.SysFont(None, 32)
        self.fuente_mediana = pygame.font.SysFont(None, 36)
        self.fuente_grande = pygame.font.SysFont(None, 48)
        self.desplazamiento_x = 0
        self.desplazamiento_y = 0

    def limpiar_pantalla(self, color):
        self.pantalla.fill(color)

    def actualizar(self):
        pygame.display.flip()

    def dibujar_laberinto(self, laberinto, tamano_celda, color_pared=COLOR_PARED_DEFAULT, color_suelo=COLOR_SUELO_DEFAULT, mostrar_rejilla=True):
        for y, fila in enumerate(laberinto):
            for x, celda in enumerate(fila):
                px = self.desplazamiento_x + x * tamano_celda
                py = self.desplazamiento_y + y * tamano_celda
                rect = pygame.Rect(px, py, tamano_celda, tamano_celda)
                if celda == 1:
                    color = color_pared
                elif celda == 2:
                    color = (255, 150, 0)  # entrada
                elif celda == 3:
                    color = (0, 255, 0)  # salida
                else:
                    color = color_suelo
                pygame.draw.rect(self.pantalla, color, rect)
                if mostrar_rejilla:
                    pygame.draw.rect(self.pantalla, (40, 40, 40), rect, 1)

    def dibujar_jugador(self, x, y, tamano):
        pygame.draw.circle(self.pantalla, COLOR_JUGADOR, (self.desplazamiento_x + x + tamano // 2, self.desplazamiento_y + y + tamano // 2), tamano // 2)

    def dibujar_enemigo(self, x, y, tamano, color=COLOR_ENEMIGO):
        pygame.draw.circle(self.pantalla, color, (self.desplazamiento_x + x + tamano // 2, self.desplazamiento_y + y + tamano // 2), tamano // 2)

    def dibujar_estrella(self, x, y, tamano):
        rect = pygame.Rect(self.desplazamiento_x + x + tamano * 0.25, self.desplazamiento_y + y + tamano * 0.25, tamano * 0.5, tamano * 0.5)
        pygame.draw.rect(self.pantalla, (255, 215, 0), rect)

    def dibujar_interfaz(self, vidas, puntos, x=30, y=24):
        t_vidas = self.fuente_interfaz.render(f"Vidas: {vidas}", True, (255, 255, 255))
        t_puntos = self.fuente_interfaz.render(f"Puntos:  {puntos}", True, (255, 255, 255))
        self.pantalla.blit(t_vidas, (x, y))
        self.pantalla.blit(t_puntos, (self.ancho - t_puntos.get_width() - 30, y))

    def dibujar_potenciador(self, x, y, tamano):
        dim = tamano * 0.5
        desp = (tamano - dim) / 2
        rect = pygame.Rect(self.desplazamiento_x + x + desp, self.desplazamiento_y + y + desp, dim, dim)
        pygame.draw.rect(self.pantalla, (255, 255, 0), rect)

    def dibujar_texto(self, texto, x, y, tamano_fuente, color=(255, 255, 255)):
        fuente = pygame.font.SysFont(None, tamano_fuente)
        superficie = fuente.render(texto, True, color)
        self.pantalla.blit(superficie, (x, y))

    # UI básica en pygame
    def input_texto(self, titulo, prompt, max_len=16):
        """Entrada de texto simple dentro del juego."""
        clock = pygame.time.Clock()
        fuente = self.fuente_mediana
        texto = ""
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return None
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return None
                    elif e.key == pygame.K_RETURN:
                        return texto.strip() or None
                    elif e.key == pygame.K_BACKSPACE:
                        texto = texto[:-1]
                    else:
                        if len(texto) < max_len and 32 <= e.key <= 126:
                            texto += e.unicode

            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.pantalla.blit(overlay, (0, 0))

            box_w, box_h = 520, 220
            box_x = (self.ancho - box_w) // 2
            box_y = (self.alto - box_h) // 2
            pygame.draw.rect(self.pantalla, (30, 30, 30), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(self.pantalla, (200, 200, 200), (box_x, box_y, box_w, box_h), 2)

            t_titulo = self.fuente_grande.render(titulo, True, (255, 255, 0))
            self.pantalla.blit(t_titulo, (box_x + 20, box_y + 15))

            t_prompt = fuente.render(prompt, True, (220, 220, 220))
            self.pantalla.blit(t_prompt, (box_x + 20, box_y + 70))

            t_input = self.fuente_interfaz.render(texto + "_", True, (255, 255, 255))
            self.pantalla.blit(t_input, (box_x + 20, box_y + 120))

            pygame.display.flip()
            clock.tick(30)

    def confirmar(self, titulo, mensaje):
        """Confirmación simple (True/False)."""
        clock = pygame.time.Clock()
        seleccionado = 0  # 0=Sí, 1=No
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    return False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        return False
                    if e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                        seleccionado = 1 - seleccionado
                    if e.key == pygame.K_RETURN:
                        return seleccionado == 0

            overlay = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.pantalla.blit(overlay, (0, 0))

            box_w, box_h = 520, 220
            box_x = (self.ancho - box_w) // 2
            box_y = (self.alto - box_h) // 2
            pygame.draw.rect(self.pantalla, (30, 30, 30), (box_x, box_y, box_w, box_h))
            pygame.draw.rect(self.pantalla, (200, 200, 200), (box_x, box_y, box_w, box_h), 2)

            t_titulo = self.fuente_grande.render(titulo, True, (255, 255, 0))
            self.pantalla.blit(t_titulo, (box_x + 20, box_y + 15))

            t_msj = self.fuente_mediana.render(mensaje, True, (220, 220, 220))
            self.pantalla.blit(t_msj, (box_x + 20, box_y + 80))

            opciones = ["[ Sí ]", "[ No ]"]
            for i, txt in enumerate(opciones):
                color = (255, 255, 0) if i == seleccionado else (200, 200, 200)
                t_opt = self.fuente_mediana.render(txt, True, color)
                self.pantalla.blit(t_opt, (box_x + 150 + i * 140, box_y + 140))

            pygame.display.flip()
            clock.tick(30)
