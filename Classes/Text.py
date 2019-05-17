import pygame
from gameObject import gameObject

class Text(gameObject):
    def __init__(self, text, pos, text_color, size, font, show=True, lifespan=False, link=[], var_link=False, update_pos=True):
        super(Text, self).__init__(pos, [0,0], text_color, show, link)
        self.text = text
        self.original_text = text
        if var_link:
            self.text = self.original_text + str(var_link()) 
        self.text_size = size
        self.font = font
        self.var_link = var_link
        self.update_pos = update_pos
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float("inf")
        self.age = 0
        
        self.font_object = pygame.font.SysFont(self.font, self.text_size)
        self.text_object = self.font_object.render(self.text, True, self.color)
        self.text_obj_size = self.font_object.size(self.text)
        
    def update(self):
        super(Text, self).update()
        self.age += 1
        
        if self.var_link:
            self.text = self.original_text + str(self.var_link()) 
        
    def draw(self, surface):
        if self.age <= self.lifespan and self.show:
            self.font_object = pygame.font.SysFont(self.font, self.text_size)
            if self.update_pos:
                self.text_obj_size = self.font_object.size(self.text)
            self.text_object = self.font_object.render(self.text, True, self.color)
            surface.blit(self.text_object, [self.pos[0] - self.text_obj_size[0] / 2, self.pos[1] - self.text_obj_size[1] / 2])
            
    def set_text(self, text):
        self.text = text
        return text
        
    def set_text_size(self, size):
        self.text_size = size
        return size
        
    def set_font(self, font):
        self.font = font
        return font
        
    def set_original_text(self, text):
        self.original_text = text
        return text
        
    def set_var_link(self, link):
        self.var_link = link
        return link
        
    def get_text(self):
        return self.text
        
    def get_font(self):
        return self.font
        
    def get_lifespan(self): 
        return self.get_lifespan
        
    def get_age(self):
        return self.age
        
    def get_original_text(self):
        return self.original_text