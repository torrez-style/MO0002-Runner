"""
Gestor de sonidos con fallback silencioso
"""
import pygame
import os
from src.data.file_manager import load_json

class SimpleSoundManager:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._initialize_mixer()
        self._load_sounds()
    
    def _initialize_mixer(self):
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.mixer_available = True
        except pygame.error:
            self.mixer_available = False
    
    def _load_sounds(self):
        sound_files = {
            'move': 'assets/sounds/move.wav',
            'star': 'assets/sounds/star.wav',
            'hit': 'assets/sounds/hit.wav',
            'win': 'assets/sounds/win.wav'
        }
        for name, path in sound_files.items():
            try:
                if os.path.exists(path) and self.mixer_available:
                    self.sounds[name] = pygame.mixer.Sound(path)
                else:
                    self.sounds[name] = None
            except pygame.error:
                self.sounds[name] = None
    
    def play_move(self):
        self._play_sound('move')
    
    def play_star(self):
        self._play_sound('star')
    
    def play_hit(self):
        self._play_sound('hit')
    
    def play_win(self):
        self._play_sound('win')
    
    def _play_sound(self, name):
        if self.enabled and self.sounds.get(name) and self.mixer_available:
            try:
                self.sounds[name].play()
            except pygame.error:
                pass
    
    def toggle_sounds(self):
        self.enabled = not self.enabled
        return self.enabled
    
    def set_enabled(self, enabled):
        self.enabled = enabled

# Instancia global
sound_manager = SimpleSoundManager()