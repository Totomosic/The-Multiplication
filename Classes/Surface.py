import pygame
from gameObject import gameObject
from Text import Text

Updates_per_second = 60

class Surface(gameObject):
    def __init__(self, pos, size, color, alpha, show=True, link=[]):
        super(Surface, self).__init__(pos, size, color, show, link)
        self.alpha = alpha
        self.texts = []
        
        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        
    def update(self):
        super(Surface, self).update()
    
    def draw(self, surface):
        self.surface.fill(self.color)
        if self.show:
            surface.blit(self.surface, self.pos) 
            
            for text in self.texts:
                text.set_pos([self.pos[0] + text.get_displacement()[0], self.pos[1] + text.get_displacement()[1]])
                text.update()
                text.draw(surface)    
                
            if self.border:
                self.draw_border(surface)  
            
    def add_text(self, text, rel_pos, color, size, font, show=True, lifespan=False, link=[], var_link=False):
        text = Text(str(text), rel_pos, color, size, font, show, lifespan, link, var_link=False)
        text.set_displacement(rel_pos)
        self.texts.append(text)
        return text
             
    def set_size(self, size):
        self.surface = pygame.Surface(size)
        self.surface.set_alpha(self.alpha)
        
    def set_alpha(self, alpha):
        self.alpha = alpha
        self.surface.set_alpha(alpha)
      
    def get_alpha(self):
        return self.alpha
        
    def get_surface(self):
        return self.surface
          