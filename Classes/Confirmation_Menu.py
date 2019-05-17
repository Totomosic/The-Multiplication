import pygame
from gameObject import gameObject
from Button import Button
from Surface import Surface
from Text import Text

class Confirmation_Menu(Surface):
    def __init__(self, text, pos, size, color, alpha, functions):
        super(Confirmation_Menu, self).__init__(pos, size, color, alpha)
        self.functions = functions + [lambda: self.set_response(True)]
        self.response_received = False
        
        self.main_text = Text(str(text), [self.pos[0] + self.size[0] / 2, self.pos[1] + self.size[1] / 2], (255,255,255), 20, "tahoma")
        self.confirm_button = Button([self.pos[0] + self.size[0] * 0.1, self.pos[1] + self.size[1] * 0.95], [self.size[0] * 0.35, self.size[1] * 0.3], (0,200,0), (0,255,0), self.alpha, self.functions)
        self.confirm_button.add_text("Confirm", [self.confirm_button.get_size()[0] / 2, self.confirm_button.get_size()[1] / 2], (255,255,255), 20, "tahoma")
        self.cancel_button = Button([self.pos[0] + self.size[0] * 0.5, self.pos[1] + self.size[1] * 0.95], [self.size[0] * 0.35, self.size[1] * 0.3], (200,0,0), (255,0,0), self.alpha, [lambda: self.set_response(True)])
        self.cancel_button.add_text("Cancel", [self.cancel_button.get_size()[0] / 2, self.cancel_button.get_size()[1] / 2], (255,255,255), 20, "tahoma")
        
    def update(self):
        super(Confirmation_Menu, self).update()
        
    def draw(self, surface):
        super(Confirmation_Menu, self).draw(surface)
        self.main_text.update()
        self.main_text.draw(surface)
        self.confirm_button.update()
        self.confirm_button.draw(surface)
        self.cancel_button.update()
        self.cancel_button.draw(surface)
        
    def set_response(self, bool):
        self.response_received = bool
        
    def get_response(self): 
        return self.response_received