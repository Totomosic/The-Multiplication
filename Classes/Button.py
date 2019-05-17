import pygame
from gameObject import gameObject
from Text import Text
from Timer import Timer

Updates_per_second = 60

class Button(gameObject):
    def __init__(self, pos, size, color, active_color, alpha, functions, show=True, link=[]):
        super(Button, self).__init__(pos, size, color, show, link)
        self.active_color = active_color
        self.alpha = alpha
        self.functions = functions
        self.prev_clicked = False
        self.updated = False
        
        self.updatable = False
        
        self.texts = []
        self.update_delay = Timer(0.1, [lambda: self.able_to_update()], True)
        
        self.surface = pygame.Surface(self.size)
        self.surface.set_alpha(self.alpha)
        self.surface.fill(self.color)
        
    def update(self):
        super(Button, self).update()
        self.update_delay.start()
        
        self.update_delay.update()
        
        if self.show and self.updatable:    
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()
            
            if self.collision([mouse_pos[0], mouse_pos[1], 0, 0]):
                self.surface.fill(self.active_color)
                if mouse_pressed[0] == 1 and not self.prev_clicked:
                    self.prev_clicked = True
                    for function in self.functions:
                        function()                   
                elif mouse_pressed[0] == 0:
                    self.prev_clicked = False
            else:
                self.surface.fill(self.color)
                        
            self.updated = True
                    
    def draw(self, surface):
        if self.show:
            surface.blit(self.surface, self.pos)
        
        if not self.updated:
            self.loop_count = 0
        self.updated = False
        
        for text in self.texts:
            text.set_pos([self.pos[0] + text.get_displacement()[0], self.pos[1] + text.get_displacement()[1]])
            text.update()
            text.draw(surface)
            
    def able_to_update(self):
        self.updatable = True
        
    def add_text(self, text, rel_pos, color, size, font, show=True, lifespan=False, link=[], var_link=[]):
        text = Text(text, rel_pos, color, size, font, show, lifespan, link, var_link)
        text.set_displacement(rel_pos)
        self.texts.append(text)
        return text
        
    def set_size(self, size):
        self.size = size
        self.surface = pygame.Surface(self.size)
        
    def set_alpha(self, alpha):
        self.alpha = alpha
        self.surface.set_alpha(self.alpha)
        
    def set_updatable(self, bool):
        self.updatable = bool
        if not self.updatable:
            self.update_delay.reset(True)
        
    def get_updatable(self):
        return self.updatable
        
    def get_alpha(self):
        return self.alpha        