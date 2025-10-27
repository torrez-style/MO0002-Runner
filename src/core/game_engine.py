"""
Motor principal del juego Maze Runner
Implementa el patrón Singleton y maneja el ciclo principal del juego

MO0002 - Programación I - Universidad de Costa Rica
Autores: Wendy Ulate, Manyel Torrez, Luis Álvarez, Kendall Alvarado
"""

import pygame
import sys
from enum import Enum
from typing import Optional

from config.settings import settings
from src.core.game_state import GameStateManager, GameState
from src.audio.sound_manager import SoundManager
from src.ui.menu import MenuPrincipal
from src.ui.game_view import GameView
from src.world.events import EventManager


class GameEngine:
    """
    Motor principal del juego - Implementa patrón Singleton
    Coordina todos los subsistemas del juego
    """
    
    _instance: Optional['GameEngine'] = None
    _initialized: bool = False
    
    def __new__(cls) -> 'GameEngine':
        """Implementa el patrón Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa el motor del juego (solo una vez)"""
        if GameEngine._initialized:
            return
        
        # Inicializar Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Configurar pantalla
        self.screen = pygame.display.set_mode((
            settings.SCREEN_WIDTH, 
            settings.SCREEN_HEIGHT
        ))
        pygame.display.set_caption(settings.WINDOW_TITLE)
        
        # Inicializar subsistemas
        self.clock = pygame.time.Clock()
        self.event_manager = EventManager()
        self.sound_manager = SoundManager()
        self.state_manager = GameStateManager()
        
        # Inicializar vistas
        self.menu = MenuPrincipal(self.screen, self.event_manager)
        self.game_view = GameView(self.screen, self.event_manager)
        
        # Variables de control
        self.running = True
        self.delta_time = 0.0
        
        GameEngine._initialized = True
    
    def run(self) -> None:
        """
        Ciclo principal del juego
        Maneja eventos, actualiza lógica y renderiza
        """
        print("🎮 Iniciando Maze Runner...")
        
        while self.running:
            # Calcular delta time
            self.delta_time = self.clock.tick(settings.FPS) / 1000.0
            
            # Manejar eventos
            self._handle_events()
            
            # Actualizar lógica
            self._update(self.delta_time)
            
            # Renderizar
            self._render()
            
            # Actualizar pantalla
            pygame.display.flip()
        
        self._cleanup()
    
    def _handle_events(self) -> None:
        """Maneja todos los eventos de Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Delegar eventos según el estado actual
            current_state = self.state_manager.current_state
            
            if current_state == GameState.MENU:
                self.menu.handle_event(event)
            elif current_state == GameState.PLAYING:
                self.game_view.handle_event(event)
            elif current_state == GameState.PAUSED:
                self._handle_pause_events(event)
            elif current_state == GameState.GAME_OVER:
                self._handle_game_over_events(event)
            elif current_state == GameState.HALL_OF_FAME:
                self._handle_hall_of_fame_events(event)
    
    def _update(self, delta_time: float) -> None:
        """Actualiza la lógica del juego"""
        current_state = self.state_manager.current_state
        
        if current_state == GameState.MENU:
            self.menu.update(delta_time)
        elif current_state == GameState.PLAYING:
            self.game_view.update(delta_time)
        elif current_state == GameState.PAUSED:
            pass  # No hay actualización en pausa
        elif current_state == GameState.GAME_OVER:
            pass  # Manejar lógica de game over
        elif current_state == GameState.HALL_OF_FAME:
            pass  # Manejar lógica de salón de la fama
    
    def _render(self) -> None:
        """Renderiza el estado actual del juego"""
        # Limpiar pantalla
        self.screen.fill(settings.COLORS['background'])
        
        current_state = self.state_manager.current_state
        
        if current_state == GameState.MENU:
            self.menu.render()
        elif current_state == GameState.PLAYING:
            self.game_view.render()
        elif current_state == GameState.PAUSED:
            self._render_pause_screen()
        elif current_state == GameState.GAME_OVER:
            self._render_game_over_screen()
        elif current_state == GameState.HALL_OF_FAME:
            self._render_hall_of_fame_screen()
    
    def _handle_pause_events(self, event: pygame.event.Event) -> None:
        """Maneja eventos en estado de pausa"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(GameState.PLAYING)
    
    def _handle_game_over_events(self, event: pygame.event.Event) -> None:
        """Maneja eventos en game over"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state_manager.change_state(GameState.PLAYING)
                self.game_view.restart_game()
            elif event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(GameState.MENU)
    
    def _handle_hall_of_fame_events(self, event: pygame.event.Event) -> None:
        """Maneja eventos en salón de la fama"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(GameState.MENU)
    
    def _render_pause_screen(self) -> None:
        """Renderiza la pantalla de pausa"""
        # Renderizar juego con overlay de pausa
        self.game_view.render()
        
        # Overlay semi-transparente
        overlay = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Texto de pausa
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSA", True, settings.COLORS['text'])
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        # Instrucción
        font_small = pygame.font.Font(None, 36)
        instruction = font_small.render("Presiona ESC para continuar", True, settings.COLORS['menu_normal'])
        instruction_rect = instruction.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 + 60))
        self.screen.blit(instruction, instruction_rect)
    
    def _render_game_over_screen(self) -> None:
        """Renderiza la pantalla de game over"""
        self.screen.fill((30, 0, 0))  # Fondo rojo oscuro
        
        font_title = pygame.font.Font(None, 96)
        title = font_title.render("GAME OVER", True, (255, 100, 100))
        title_rect = title.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 - 50))
        self.screen.blit(title, title_rect)
        
        font_info = pygame.font.Font(None, 48)
        score_text = font_info.render(f"Puntuación: {self.game_view.get_final_score()}", True, settings.COLORS['text'])
        score_rect = score_text.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 + 20))
        self.screen.blit(score_text, score_rect)
        
        font_instruction = pygame.font.Font(None, 36)
        instruction = font_instruction.render("ENTER: Reintentar    ESC: Menú", True, settings.COLORS['menu_normal'])
        instruction_rect = instruction.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT//2 + 80))
        self.screen.blit(instruction, instruction_rect)
    
    def _render_hall_of_fame_screen(self) -> None:
        """Renderiza el salón de la fama"""
        self.screen.fill((0, 0, 50))  # Fondo azul oscuro
        
        font_title = pygame.font.Font(None, 72)
        title = font_title.render("SALÓN DE LA FAMA", True, settings.COLORS['menu_selected'])
        title_rect = title.get_rect(center=(settings.SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # TODO: Implementar lógica de carga y visualización de puntuaciones
        
        font_instruction = pygame.font.Font(None, 36)
        instruction = font_instruction.render("ESC: Volver al menú", True, settings.COLORS['menu_normal'])
        instruction_rect = instruction.get_rect(center=(settings.SCREEN_WIDTH//2, settings.SCREEN_HEIGHT - 50))
        self.screen.blit(instruction, instruction_rect)
    
    def _cleanup(self) -> None:
        """Limpia recursos y cierra el juego"""
        print("🛑 Cerrando Maze Runner...")
        pygame.quit()
        sys.exit()
    
    def change_state(self, new_state: GameState) -> None:
        """Cambia el estado del juego"""
        self.state_manager.change_state(new_state)
    
    def quit_game(self) -> None:
        """Termina el juego"""
        self.running = False
