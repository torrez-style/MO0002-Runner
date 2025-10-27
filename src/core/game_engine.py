"""
Motor del juego: flujo completo con entrada de nombre, admin y confirmación de salida
"""
import pygame
from config.settings import settings
from src.core.game_state import GameStateManager, GameState
from src.world.events import EventManager
from src.ui.menu import MenuPrincipal
from src.ui.game_view import GameView
from src.ui.hall_of_fame import HallOfFameView
from src.ui.name_input import NameInputView
from src.ui.admin_view import AdminView
from src.ui.confirm_dialog import ConfirmDialog
from src.core.game_bootstrap import GameBootstrap
from src.audio.sound_manager import sound_manager

class GameEngine:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.WINDOW_TITLE)
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.events = EventManager(enable_logging=False)
        self.state = GameStateManager(initial_state=GameState.MENU)
        
        # Vistas
        self.menu = MenuPrincipal(self.screen, self.events)
        self.view = GameView(self.screen, self.events)
        self.hof = HallOfFameView(self.screen)
        self.name_input = NameInputView(self.screen)
        self.admin = AdminView(self.screen)
        self.confirm_dialog = None
        self.bootstrap = GameBootstrap()
        
        # Estado de confirmación
        self.confirming_exit = False
        self.pending_player_name = "SULA"
        
        # Cargar nivel 1
        self.level_loaded = self.bootstrap.load_levels()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                else:
                    if self.confirming_exit:
                        if self.confirm_dialog:
                            result = self.confirm_dialog.handle_event(e)
                            if result == "YES":
                                running = False
                            elif result == "NO":
                                self.confirming_exit = False
                                self.confirm_dialog = None
                    
                    elif self.state.current_state == GameState.MENU:
                        self.menu.handle_event(e)
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                            opcion = self.menu.options[self.menu.index]
                            if opcion == "JUGAR":
                                self.state.change_state(GameState.NAME_INPUT, force=True)
                            elif opcion == "SALON DE LA FAMA":
                                self.state.change_state(GameState.HALL_OF_FAME, force=True)
                            elif opcion == "ADMINISTRACION":
                                self.admin.reset_state()
                                self.state.change_state(GameState.ADMIN, force=True)
                            elif opcion == "SALIR":
                                self.confirm_dialog = ConfirmDialog(self.screen, "Salir del juego?")
                                self.confirming_exit = True
                    
                    elif self.state.current_state == GameState.NAME_INPUT:
                        result = self.name_input.handle_event(e)
                        if result in ["CONFIRM", "CONFIRM_DEFAULT"]:
                            self.pending_player_name = self.name_input.get_name()
                            self.bootstrap.set_player_name(self.pending_player_name)
                            self.state.change_state(GameState.PLAYING, force=True)
                        elif result == "CANCEL":
                            self.state.change_state(GameState.MENU, force=True)
                    
                    elif self.state.current_state == GameState.PLAYING:
                        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                            self.state.change_state(GameState.MENU, force=True)
                        result = self.bootstrap.handle_event(e)
                        if result == "BACK_TO_MENU":
                            self.state.change_state(GameState.MENU, force=True)
                    
                    elif self.state.current_state == GameState.HALL_OF_FAME:
                        action = self.hof.handle_event(e)
                        if action == "BACK":
                            self.state.change_state(GameState.MENU, force=True)
                    
                    elif self.state.current_state == GameState.ADMIN:
                        result = self.admin.handle_event(e)
                        if result in ["CANCEL", "ACCESS_DENIED", "BACK"]:
                            self.state.change_state(GameState.MENU, force=True)
            
            # Update
            if self.state.current_state == GameState.MENU:
                self.menu.update(dt)
            elif self.state.current_state == GameState.NAME_INPUT:
                self.name_input.update(dt)
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.update()
            
            # Render
            self.screen.fill((0,0,0))
            
            if self.state.current_state == GameState.MENU:
                self.menu.render()
            elif self.state.current_state == GameState.NAME_INPUT:
                self.name_input.render()
            elif self.state.current_state == GameState.PLAYING:
                self.bootstrap.render(self.screen)
            elif self.state.current_state == GameState.HALL_OF_FAME:
                self.hof.render()
            elif self.state.current_state == GameState.ADMIN:
                self.admin.render()
            
            # Overlay de confirmación
            if self.confirming_exit and self.confirm_dialog:
                self.confirm_dialog.render()
            
            pygame.display.flip()
        pygame.quit()