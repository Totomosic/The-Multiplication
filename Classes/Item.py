import pygame

class Item(object):
    def __init__(self, name, desc, type, rank, image, image_size, level, mod_slots=2):
        self.name = name
        self.desc = desc
        self.type = type
        self.rank = rank
        self.level = level
        self.direction = 1
        self.size = image_size
        
        self.mod_slots = mod_slots
        self.mod_list = []
        
        self.loop_count = 0
        self.image = image
        self.image_reverse = pygame.transform.flip(self.image, True, False)
        
        self.color = (0,0,0)
        if self.get_rank() == 0:
            self.color = (100,100,100)
        elif self.get_rank() == 1:
            self.color = (0,200,0)
        elif self.get_rank() == 2:
            self.color = (0,0,200)
        elif self.get_rank() == 3:
            self.color = (160,32,240)
        elif self.get_rank() == 4:
            self.color = (200,200,0)
            
    def update(self):
        if self.get_rank() == 0:
            self.color = (100,100,100)
        elif self.get_rank() == 1:
            self.color = (0,200,0)
        elif self.get_rank() == 2:
            self.color = (0,0,200)
        elif self.get_rank() == 3:
            self.color = (160,32,240)
        elif self.get_rank() == 4:
            self.color = (200,200,0)
            
        self.loop_count += 1
            
    def draw(self, surface, pos):
        if self.direction > 0:
            surface.blit(self.image, pos)
        else:
            surface.blit(self.image_reverse, pos)
            
    def get_name(self):
        return self.name
        
    def get_type(self):
        return self.type
        
    def get_rank(self):
        return self.rank
        
    def get_desc(self):
        return self.desc
        
    def get_size(self):
        return self.size
        
    def get_level(self):
        return self.level
        
    def get_direction(self):
        return self.direction
        
    def get_color(self):
        return self.color
        
    def get_image_list(self):
        return [self.image, self.image_reverse]
        
    def get_loop_count(self):
        return self.loop_count
        
    def get_mod_list(self):
        return self.mod_list
        
    def get_mod_slots(self):
        return self.mod_slots
        
    def set_name(self, name):
        self.name = name
        return name
        
    def set_rank(self, rank):
        self.rank = rank
        return rank
        
    def set_type(self, type):
        self.type = type
        return type
        
    def set_size(self, size):
        self.size = size
        return size
        
    def set_level(self, level):
        self.level = level
        return level
        
    def set_direction(self, direction):
        self.direction = direction
        return direction
        
    def set_image(self, image):
        self.image = image
        self.image_reverse = pygame.trasnform.flip(image)
        return image
        
    def set_mod_slots(self, slots):
        self.mod_slots = slots
        return slots
        
    def add_mod(self, mod):
        self.mod_list.append(mod)
        
    def remove_mod(self, mod):
        if mod in self.mod_list:
            self.mod_list.remove(mod)
        