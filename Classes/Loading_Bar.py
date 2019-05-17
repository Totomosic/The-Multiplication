import pygame
from gameObject import gameObject
from Surface import Surface

class Loading_Bar(gameObject):
    def __init__(self, pos, max_size, bar_color, bg_color, bar_alpha, bg_alpha, padding, show=True, link=[], var_link=False):
        super(Loading_Bar, self).__init__(pos, max_size, bar_color, show, link)
        self.bg_color = bg_color
        self.padding = padding
        self.bar_alpha = bar_alpha
        self.bg_alpha = bg_alpha
        self.var_link = var_link        
        self.current = 0
        self.max = 0
        
        self.background = pygame.Surface(self.size)
        self.background.set_alpha(self.bg_alpha)
        self.bar = pygame.Surface([self.size[0] - self.padding * 2, self.size[1] - self.padding * 2])
        self.bar.set_alpha(self.bar_alpha)
        
    def update(self):
        super(Loading_Bar, self).update()
        
        for link in self.var_link:
            if self.var_link.index(link) == 0:
                self.min = link()        
            else:
                self.max = link()
        
        bar_size = [int((float(self.min) / self.max) * (self.size[0] - self.padding * 2)), int(self.size[1] - self.padding * 2)]
        if bar_size[0] + self.padding * 2 > self.size[0]:
            bar_size = [self.size[0] - self.padding * 2, self.size[1] - self.padding * 2]
        if bar_size[0] < 0:
            bar_size = [0, self.size[1]]
        
        self.bar = pygame.Surface(bar_size)
        
        self.background.fill(self.bg_color)
        self.bar.fill(self.color)
        
    def draw(self, surface):
        if self.show:
            surface.blit(self.background, self.pos)
            surface.blit(self.bar, [self.pos[0] + self.padding, self.pos[1] + self.padding])
            
    def set_size(self, size):
        self.size = size
        self.bar = pygame.Surface([self.size[0] - self.padding * 2, self.size[1] - self.padding * 2])
        self.background = pygame.Surface(self.size)
            