"""
Pantalla de entrada de nombre del jugador
"""
import pygame

class NameInputView:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont(None, 56)
        self.font_text = pygame.font.SysFont(None, 36)
        self.font_hint = pygame.font.SysFont(None, 24)
        self.name = ""
        self.cursor_timer = 0
        self.bg_color = (20, 20, 60)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return "CONFIRM" if self.name.strip() else "CONFIRM_DEFAULT"
            elif event.key == pygame.K_ESCAPE:
                return "CANCEL"
            elif event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
            elif event.unicode.isprintable() and len(self.name) < 18:
                self.name += event.unicode
        return None
    
    def update(self, delta_time):
        self.cursor_timer += 1
    
    def render(self):
        w, h = self.screen.get_size()
        self.screen.fill(self.bg_color)
        
        title = self.font_title.render("Ingrese su nombre", True, (255, 255, 255))
        self.screen.blit(title, ((w - title.get_width())//2, int(h*0.25)))
        
        # Campo de entrada
        display_name = self.name if self.name else "SULA"
        cursor = "_" if (self.cursor_timer // 30) % 2 == 0 else " "
        text_surf = self.font_text.render(display_name + cursor, True, (255, 255, 100))
        self.screen.blit(text_surf, ((w - text_surf.get_width())//2, int(h*0.45)))
        
        # Instrucciones
        hint1 = self.font_hint.render("ENTER: Confirmar", True, (200, 200, 200))
        hint2 = self.font_hint.render("ESC: Cancelar", True, (200, 200, 200))
        hint3 = self.font_hint.render("(Vacio usa SULA por defecto)", True, (160, 160, 160))
        self.screen.blit(hint1, ((w - hint1.get_width())//2, int(h*0.65)))
        self.screen.blit(hint2, ((w - hint2.get_width())//2, int(h*0.70)))
        self.screen.blit(hint3, ((w - hint3.get_width())//2, int(h*0.78)))
    
    def get_name(self):
        return self.name.strip() if self.name.strip() else "SULA"