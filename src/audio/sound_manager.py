"""
Sistema de gestión de audio para Maze Runner
Maneja efectos de sonido y música de fondo

MO0002 - Programación I - Universidad de Costa Rica
"""

import pygame
import os
from enum import Enum
from typing import Dict, Optional
from dataclasses import dataclass

from config.settings import settings, Paths


class SoundEffect(Enum):
    """Efectos de sonido disponibles en el juego"""
    PLAYER_MOVE = "player_move.wav"
    ITEM_COLLECT = "item_collect.wav"
    PLAYER_CAUGHT = "player_caught.wav"
    POWERUP_ACTIVATE = "powerup_activate.wav"
    LEVEL_COMPLETE = "level_complete.wav"
    GAME_OVER = "game_over.wav"
    MENU_SELECT = "menu_select.wav"
    MENU_NAVIGATE = "menu_navigate.wav"


class MusicTrack(Enum):
    """Pistas de música disponibles"""
    MENU_THEME = "menu_theme.ogg"
    GAME_THEME = "game_theme.ogg"
    VICTORY_THEME = "victory_theme.ogg"


@dataclass
class AudioSettings:
    """Configuración de audio"""
    master_volume: float = 0.7
    sfx_volume: float = 0.8
    music_volume: float = 0.6
    enable_sound: bool = True
    enable_music: bool = True


class SoundManager:
    """
    Administrador de sonido del juego
    Maneja efectos de sonido y música de fondo
    """
    
    def __init__(self):
        """Inicializa el sistema de audio"""
        self.audio_settings = AudioSettings(
            master_volume=settings.MASTER_VOLUME,
            sfx_volume=settings.SFX_VOLUME,
            enable_sound=settings.ENABLE_SOUND
        )
        
        # Diccionarios para almacenar sonidos cargados
        self.sound_effects: Dict[SoundEffect, pygame.mixer.Sound] = {}
        self.music_tracks: Dict[MusicTrack, str] = {}
        
        # Estado actual
        self.current_music: Optional[MusicTrack] = None
        self.music_playing = False
        
        # Inicializar pygame mixer si no está inicializado
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        
        # Cargar sonidos
        self._load_sound_effects()
        self._load_music_tracks()
        
        print(f"🎵 Sistema de audio inicializado")
        print(f"   - Efectos de sonido: {'Habilitado' if self.audio_settings.enable_sound else 'Deshabilitado'}")
        print(f"   - Música: {'Habilitada' if self.audio_settings.enable_music else 'Deshabilitada'}")
    
    def _load_sound_effects(self) -> None:
        """Carga todos los efectos de sonido"""
        for effect in SoundEffect:
            sound_path = Paths.get_sound_path(effect.value)
            
            # Si el archivo no existe, crear un sonido placeholder
            if not os.path.exists(sound_path):
                # Crear directorio si no existe
                os.makedirs(os.path.dirname(sound_path), exist_ok=True)
                
                # Crear sonido placeholder (silencio corto)
                placeholder_sound = self._create_placeholder_sound()
                self.sound_effects[effect] = placeholder_sound
                print(f"⚠️  Sonido no encontrado: {sound_path} (usando placeholder)")
            else:
                try:
                    sound = pygame.mixer.Sound(sound_path)
                    self.sound_effects[effect] = sound
                    print(f"✓ Sonido cargado: {effect.name}")
                except pygame.error as e:
                    print(f"❌ Error cargando {effect.name}: {e}")
                    self.sound_effects[effect] = self._create_placeholder_sound()
    
    def _load_music_tracks(self) -> None:
        """Carga todas las pistas de música"""
        for track in MusicTrack:
            music_path = Paths.get_sound_path(track.value)
            
            if os.path.exists(music_path):
                self.music_tracks[track] = music_path
                print(f"✓ Música cargada: {track.name}")
            else:
                print(f"⚠️  Música no encontrada: {music_path}")
    
    def _create_placeholder_sound(self, duration_ms: int = 100) -> pygame.mixer.Sound:
        """
        Crea un sonido placeholder (silencio) para archivos faltantes
        """
        sample_rate = 22050
        frames = int(duration_ms * sample_rate / 1000)
        
        # Crear array de silencio
        silence = pygame.sndarray.make_sound(pygame.numpy.zeros((frames, 2), dtype=pygame.numpy.int16))
        return silence
    
    def play_sound(self, effect: SoundEffect, volume_multiplier: float = 1.0) -> None:
        """
        Reproduce un efecto de sonido
        
        Args:
            effect: Efecto de sonido a reproducir
            volume_multiplier: Multiplicador de volumen (0.0 - 1.0)
        """
        if not self.audio_settings.enable_sound:
            return
        
        if effect in self.sound_effects:
            sound = self.sound_effects[effect]
            final_volume = (
                self.audio_settings.master_volume * 
                self.audio_settings.sfx_volume * 
                volume_multiplier
            )
            sound.set_volume(final_volume)
            sound.play()
        else:
            print(f"⚠️  Efecto de sonido no encontrado: {effect.name}")
    
    def play_music(self, track: MusicTrack, loop: bool = True, fade_in_ms: int = 1000) -> bool:
        """
        Reproduce música de fondo
        
        Args:
            track: Pista de música a reproducir
            loop: Si debe reproducirse en bucle
            fade_in_ms: Tiempo de fade in en milisegundos
        
        Returns:
            True si se pudo reproducir, False si no
        """
        if not self.audio_settings.enable_music:
            return False
        
        if track not in self.music_tracks:
            print(f"⚠️  Pista de música no encontrada: {track.name}")
            return False
        
        try:
            # Detener música actual si hay alguna
            if self.music_playing:
                pygame.mixer.music.fadeout(500)
            
            # Cargar y reproducir nueva música
            pygame.mixer.music.load(self.music_tracks[track])
            
            # Configurar volumen
            volume = self.audio_settings.master_volume * self.audio_settings.music_volume
            pygame.mixer.music.set_volume(volume)
            
            # Reproducir con fade in
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops, fade_ms=fade_in_ms)
            
            self.current_music = track
            self.music_playing = True
            
            print(f"🎵 Reproduciendo música: {track.name}")
            return True
            
        except pygame.error as e:
            print(f"❌ Error reproduciendo música {track.name}: {e}")
            return False
    
    def stop_music(self, fade_out_ms: int = 1000) -> None:
        """Detiene la música de fondo"""
        if self.music_playing:
            pygame.mixer.music.fadeout(fade_out_ms)
            self.music_playing = False
            self.current_music = None
            print("🔇 Música detenida")
    
    def pause_music(self) -> None:
        """Pausa la música de fondo"""
        if self.music_playing:
            pygame.mixer.music.pause()
            print("⏸️ Música pausada")
    
    def resume_music(self) -> None:
        """Reanuda la música de fondo"""
        if self.music_playing:
            pygame.mixer.music.unpause()
            print("▶️ Música reanudada")
    
    def set_master_volume(self, volume: float) -> None:
        """Establece el volumen maestro (0.0 - 1.0)"""
        self.audio_settings.master_volume = max(0.0, min(1.0, volume))
        
        # Actualizar volumen de música si está reproduciéndose
        if self.music_playing:
            music_volume = self.audio_settings.master_volume * self.audio_settings.music_volume
            pygame.mixer.music.set_volume(music_volume)
        
        print(f"🔊 Volumen maestro: {self.audio_settings.master_volume:.1f}")
    
    def set_sfx_volume(self, volume: float) -> None:
        """Establece el volumen de efectos de sonido (0.0 - 1.0)"""
        self.audio_settings.sfx_volume = max(0.0, min(1.0, volume))
        print(f"🔊 Volumen SFX: {self.audio_settings.sfx_volume:.1f}")
    
    def set_music_volume(self, volume: float) -> None:
        """Establece el volumen de música (0.0 - 1.0)"""
        self.audio_settings.music_volume = max(0.0, min(1.0, volume))
        
        # Actualizar volumen si hay música reproduciéndose
        if self.music_playing:
            final_volume = self.audio_settings.master_volume * self.audio_settings.music_volume
            pygame.mixer.music.set_volume(final_volume)
        
        print(f"🔊 Volumen música: {self.audio_settings.music_volume:.1f}")
    
    def toggle_sound(self) -> bool:
        """Activa/desactiva efectos de sonido"""
        self.audio_settings.enable_sound = not self.audio_settings.enable_sound
        status = "habilitados" if self.audio_settings.enable_sound else "deshabilitados"
        print(f"🔊 Efectos de sonido {status}")
        return self.audio_settings.enable_sound
    
    def toggle_music(self) -> bool:
        """Activa/desactiva música de fondo"""
        self.audio_settings.enable_music = not self.audio_settings.enable_music
        
        if not self.audio_settings.enable_music and self.music_playing:
            self.stop_music()
        
        status = "habilitada" if self.audio_settings.enable_music else "deshabilitada"
        print(f"🎵 Música {status}")
        return self.audio_settings.enable_music
    
    def get_audio_info(self) -> dict:
        """Obtiene información del estado del audio"""
        return {
            'master_volume': self.audio_settings.master_volume,
            'sfx_volume': self.audio_settings.sfx_volume,
            'music_volume': self.audio_settings.music_volume,
            'sound_enabled': self.audio_settings.enable_sound,
            'music_enabled': self.audio_settings.enable_music,
            'current_music': self.current_music.name if self.current_music else None,
            'music_playing': self.music_playing,
            'loaded_sounds': len(self.sound_effects),
            'loaded_music': len(self.music_tracks)
        }
    
    def cleanup(self) -> None:
        """Limpia recursos de audio"""
        self.stop_music(0)
        pygame.mixer.stop()  # Detiene todos los sonidos
        print("🧪 Sistema de audio limpiado")
