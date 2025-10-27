"""
Motor del juego: navegación correcta desde menú según opción seleccionada
"""
import pygame
from config.settings import settings
from src.core.game_state import GameStateManager, GameState
from src.world.events import EventManager
from src.ui.menu import MenuPrincipal
from src.ui.game_view import GameView
from src.ui.hall_of_fame import HallOfFameView
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
        self.hof = HallOfFameView(self.screen)
        self.bootstrap = GameBootstrap()
        
        # Cargar nivel 1 al iniciar
        self.level_loaded = self.bootstrap.load_levels()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                else:
                    if self.state.current_state == GameState.MENU:
                        self.menu.handle_event(e)
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                            opcion = self.menu.options[self.menu.index]
                            if opcion == "JUGAR":
                                self.state.change_state(GameState.PLAYING, force=True)
                            elif opcion == "SALON DE LA FAMA":
                                self.state.change_state(GameState.HALL_OF_FAME, force=True)
                            elif opcion == "ADMINISTRACION":
                                # futuro: estado de administración
                                pass
                            elif opcion == "SALIR":
                                running = False
                    elif self.state.current_state == GameState.PLAYING:
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                            self.state.change_state(GameState.MENU, force=True)
                        self.bootstrap.handle_event(e)
                    elif self.state.current_state == GameState.HALL_OF_FAME:
                        action = self.hof.handle_event(e)
                        if action == "BACK":
                            self.state.change_state(GameState.MENU, force=True)
            
            # Update
            if self.state.current_state == GameState.MENU:
                self.menu.update(dt)
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.update()
            
            # Render
            self.screen.fill((0,0,0))
            if self.state.current_state == GameState.MENU:
                self.menu.render()
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.render(self.screen)
            elif self.state.current_state == GameState.HALL_OF_FAME:
                self.hof.render()
            
            pygame.display.flip()
        pygame.quit()
