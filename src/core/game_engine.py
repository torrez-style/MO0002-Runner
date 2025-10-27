"""
Motor del juego: conecta menú, carga nivel 1 y renderiza
"""
import pygame
from config.settings import settings
from src.core.game_state import GameStateManager, GameState
from src.world.events import EventManager
from src.ui.menu import MenuPrincipal
from src.ui.game_view import GameView
from src.core.game_bootstrap import GameBootstrap

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.events = EventManager(enable_logging=False)
        self.state = GameStateManager(initial_state=GameState.MENU)
        
        self.menu = MenuPrincipal(self.screen, self.events)
        self.view = GameView(self.screen, self.events)
        self.bootstrap = GameBootstrap()
        
        # Cargar nivel 1 al iniciar; se mostrará cuando se pase a PLAYING
        self.level_loaded = self.bootstrap.load_levels()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                else:
                    # Manejo básico: ENTER cambia de MENU a PLAYING
                    if self.state.current_state == GameState.MENU:
                        self.menu.handle_event(e)
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                            self.state.change_state(GameState.PLAYING, force=True)
                    elif self.state.current_state == GameState.PLAYING:
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                            self.state.change_state(GameState.MENU, force=True)
                        self.view.handle_event(e)
            
            # Update
            if self.state.current_state == GameState.MENU:
                self.menu.update(dt)
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.update()
                self.view.update(dt)
            
            # Render
            self.screen.fill((0,0,0))
            if self.state.current_state == GameState.MENU:
                self.menu.render()
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.render(self.screen)
            
            pygame.display.flip()
        pygame.quit()
