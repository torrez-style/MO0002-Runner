"""
Diálogo de confirmación reutilizable
"""
import pygame

class ConfirmDialog:
    def __init__(self, screen, message="Confirmar?"):
        self.screen = screen
        self.message = message
        self.font_title = pygame.font.SysFont(None, 48)
        self.font_opt = pygame.font.SysFont(None, 36)
        self.options = ["SI", "NO"]
        self.index = 1  # Default a NO
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.index = 0
            elif event.key == pygame.K_RIGHT:
                self.index = 1
            elif event.key == pygame.K_RETURN:
                return "YES" if self.index == 0 else "NO"
            elif event.key == pygame.K_ESCAPE:
                return "NO"
        return None
    
    def render(self):
        w, h = self.screen.get_size()
        # Overlay semitransparente
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Mensaje
        msg_surf = self.font_title.render(self.message, True, (255, 255, 255))
        self.screen.blit(msg_surf, ((w - msg_surf.get_width())//2, int(h*0.35)))
        
        # Opciones
        y = int(h*0.55)
        total_width = sum(self.font_opt.size(opt)[0] for opt in self.options) + 60
        start_x = (w - total_width) // 2
        x = start_x
        
        for i, opt in enumerate(self.options):
            color = (255, 255, 0) if i == self.index else (200, 200, 200)
            surf = self.font_opt.render(opt, True, color)
            self.screen.blit(surf, (x, y))
            x += surf.get_width() + 60