"""
Pantalla de administración con contraseña y utilidades
"""
import pygame
from src.data.file_manager import load_json, save_json, SCORES_FILE
from src.audio.sound_manager import sound_manager

class AdminView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_text = pygame.font.SysFont(None, 32)
        self.font_hint = pygame.font.SysFont(None, 24)
        self.state = "PASSWORD"  # PASSWORD, MENU, CONFIRM_RESET
        self.password = ""
        self.attempts = 0
        self.max_attempts = 3
        self.menu_index = 0
        self.menu_options = [
            "Reset Salon de la Fama",
            "Toggle Sonidos",
            "Listar Laberintos",
            "Salir"
        ]
        self.bg_color = (40, 0, 0)
        self.confirm_yes = True
    
    def handle_event(self, event):
        if self.state == "PASSWORD":
            return self._handle_password_event(event)
        elif self.state == "MENU":
            return self._handle_menu_event(event)
        elif self.state == "CONFIRM_RESET":
            return self._handle_confirm_reset_event(event)
        return None
    
    def _handle_password_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.password == "admin":
                    self.state = "MENU"
                    self.password = ""
                else:
                    self.attempts += 1
                    self.password = ""
                    if self.attempts >= self.max_attempts:
                        return "ACCESS_DENIED"
            elif event.key == pygame.K_ESCAPE:
                return "CANCEL"
            elif event.key == pygame.K_BACKSPACE:
                self.password = self.password[:-1]
            elif event.unicode.isprintable() and len(self.password) < 20:
                self.password += event.unicode
        return None
    
    def _handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_index = (self.menu_index - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.menu_index = (self.menu_index + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                return self._execute_menu_option()
            elif event.key == pygame.K_ESCAPE:
                return "BACK"
        return None
    
    def _handle_confirm_reset_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                self.confirm_yes = not self.confirm_yes
            elif event.key == pygame.K_RETURN:
                if self.confirm_yes:
                    save_json(SCORES_FILE, [])
                    self.state = "MENU"
                    return "HALL_RESET"
                else:
                    self.state = "MENU"
                    return None
            elif event.key == pygame.K_ESCAPE:
                self.state = "MENU"
                return None
        return None
    
    def _execute_menu_option(self):
        option = self.menu_options[self.menu_index]
        if option == "Reset Salon de la Fama":
            self.state = "CONFIRM_RESET"
            return None
        elif option == "Toggle Sonidos":
            sound_manager.toggle_sounds()
            return "SOUNDS_TOGGLED"
        elif option == "Listar Laberintos":
            return "LIST_LEVELS"
        elif option == "Salir":
            return "BACK"
        return None
    
    def render(self):
        w, h = self.screen.get_size()
        self.screen.fill(self.bg_color)
        
        if self.state == "PASSWORD":
            title = self.font_title.render("ADMINISTRACION", True, (255, 255, 255))
            self.screen.blit(title, ((w - title.get_width())//2, int(h*0.20)))
            
            prompt = self.font_text.render("Ingrese contraseña:", True, (255, 255, 255))
            self.screen.blit(prompt, ((w - prompt.get_width())//2, int(h*0.40)))
            
            pwd_display = "*" * len(self.password)
            pwd_surf = self.font_text.render(pwd_display, True, (255, 255, 100))
            self.screen.blit(pwd_surf, ((w - pwd_surf.get_width())//2, int(h*0.50)))
            
            if self.attempts > 0:
                error = self.font_hint.render(f"Contraseña incorrecta ({self.attempts}/{self.max_attempts})", True, (255, 100, 100))
                self.screen.blit(error, ((w - error.get_width())//2, int(h*0.60)))
            
            hint = self.font_hint.render("ENTER: Confirmar | ESC: Cancelar", True, (200, 200, 200))
            self.screen.blit(hint, ((w - hint.get_width())//2, int(h*0.75)))
        
        elif self.state == "MENU":
            title = self.font_title.render("PANEL ADMINISTRATIVO", True, (255, 255, 255))
            self.screen.blit(title, ((w - title.get_width())//2, int(h*0.15)))
            
            y = int(h*0.35)
            for i, opt in enumerate(self.menu_options):
                color = (255, 255, 0) if i == self.menu_index else (200, 200, 200)
                surf = self.font_text.render(opt, True, color)
                self.screen.blit(surf, ((w - surf.get_width())//2, y))
                y += 40
            
            status = f"Sonidos: {'ON' if sound_manager.enabled else 'OFF'}"
            status_surf = self.font_hint.render(status, True, (150, 150, 255))
            self.screen.blit(status_surf, (20, h-30))
        
        elif self.state == "CONFIRM_RESET":
            title = self.font_title.render("Eliminar Salon de la Fama?", True, (255, 255, 255))
            self.screen.blit(title, ((w - title.get_width())//2, int(h*0.30)))
            
            opt_yes = self.font_text.render("SI", True, (255, 255, 0) if self.confirm_yes else (200,200,200))
            opt_no = self.font_text.render("NO", True, (255, 255, 0) if not self.confirm_yes else (200,200,200))
            
            self.screen.blit(opt_yes, (w//2 - 60, int(h*0.55)))
            self.screen.blit(opt_no, (w//2 + 20, int(h*0.55)))
