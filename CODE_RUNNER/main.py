import pygame

# Inicializar Pygame y crear la ventana
pygame.init()
ancho, alto = 600, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Juego Laberinto - Fase 2")
reloj = pygame.time.Clock()

# Bucle principal del juego
corriendo = True
while corriendo:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    ventana.fill((0, 0, 0))  # Fondo negro
    pygame.display.flip()
    reloj.tick(60)  # 60 FPS

pygame.quit()
