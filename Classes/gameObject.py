import pygame

Updates_per_second = 60

class gameObject(object):
    def __init__(self, pos, size, color, show=True, link=[]):
        self.pos = pos
        self.vel = [0,0]
        self.size = size
        self.color = color
        self.show = show
        self.link = link
        self.displacement = 0
        
        self.border = False
        
        self.loop_count = 0
        
    def update(self):
        if self.show:
            self.pos[0] += self.vel[0]
            self.pos[1] += self.vel[1]
        
        count = 0
        for link in self.link:
            if link.get_show():
                self.show = True
                count += 1
                
        if count > 0:
            self.show = True
        elif self.link:
            self.show = False
            
        self.loop_count += 1
            
    def draw(self, surface):
        if self.show:
            pygame.draw.rect(surface, self.color, [self.pos[0], self.pos[1], self.size[0], self.size[1]])
            
            if self.border:
                self.draw_border(surface)
                
    def draw_border(self, surface):
        if self.border:
            pygame.draw.lines(surface, (0,0,0), True, [[self.pos[0], self.pos[1]], [self.pos[0], self.pos[1] + self.size[1]], [self.pos[0] + self.size[0], self.pos[1] + self.size[1]], [self.pos[0] + self.size[0], self.pos[1]]], 3)
            
    def add_border(self):
        self.border = True
            
    def clone(self):
        return gameObject([self.pos[0], self.pos[1]], [self.size[0], self.size[1]], self.color, self.show, self.link)
        
    def collision(self, obj2_rect):
        obj1_rect = [self.pos[0], self.pos[1], self.size[0], self.size[1]]
        if obj1_rect[0] + obj1_rect[2] > obj2_rect[0] and obj1_rect[0] < obj2_rect[0] + obj2_rect[2] and obj1_rect[1] + obj1_rect[3] > obj2_rect[1] and obj1_rect[1] < obj2_rect[1] + obj2_rect[3]:
            return True
        return False     
        
    def xCollision(self, obj2_rect):
        obj1_rect = [self.pos[0], self.pos[1], self.size[0], self.size[1]]   
        if obj1_rect[0] + obj1_rect[2] > obj2_rect[0] and obj1_rect[0] < obj2_rect[0] + obj2_rect[2]:
            return True
        return False
        
    def yCollision(self, obj2_rect):
        obj1_rect = [self.pos[0], self.pos[1], self.size[0], self.size[1]]   
        if obj1_rect[1] + obj1_rect[3] > obj2_rect[1] and obj1_rect[1] < obj2_rect[1] + obj2_rect[3]:
            return True
        return False
        
    def set_pos(self, pos, index=False):
        self.pos = pos
        return pos
            
    def set_size(self, size, index=False):
        self.size = size
        return size
            
    def set_vel(self, vel, index=False):
        self.vel = vel
        return vel
           
    def set_color(self, color):
        self.color = color
        return color
        
    def set_show(self, show_bool):
        self.show = show_bool
        return show_bool
        
    def set_link(self, linking_object):
        self.link = linking_object
        return linking_object
        
    def set_loop_count(self, count):
        self.loop_count = count
        return count
        
    def set_displacement(self, dis):
        self.displacement = dis
        return dis
        
    def get_pos(self, index=False):
        return self.pos
            
    def get_size(self, index=False):
        return self.size
            
    def get_vel(self, index=False):
        return self.vel
            
    def get_color(self):
        return self.color
        
    def get_show(self):
        return self.show
        
    def get_link(self):
        return self.link
        
    def get_loop_count(self):
        return self.loop_count
        
    def get_displacement(self):
        return self.displacement
        
    def get_border(self):
        return self.border
        
    def toggle_show(self):
        if self.show:
            self.show = False
        else:
            self.show = True
        return self.show