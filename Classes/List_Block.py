import pygame
from Surface import Surface

class List_Block(Surface):
    def __init__(self, pos, size, color, alpha, max_items, item_spacing=2, item_list=[], show=True, link=[]):
        super(List_Block, self).__init__(pos, [size[0], size[1]], color, alpha, show, link)
        self.max_items = max_items
        self.current_item = 0
        self.current_end_item = self.max_items
        self.item_list = item_list
        self.spacing = item_spacing
        self.item_height = int((float(self.size[1]) + self.spacing) / self.max_items)
        
    def update(self):
        super(List_Block, self).update()
        self.current_end_item = self.current_item + self.max_items
        
        mouse_pos = pygame.mouse.get_pos()
        
    def draw(self, surface):
        super(List_Block, self).draw(surface)
        self.surface = pygame.Surface([self.size[0], self.size[1] + self.spacing])
        
        self.position = self.pos[1] + self.spacing
        self.item_height = (self.size[1] - (self.spacing * self.max_items)) / self.max_items
        
        for x in range(self.current_item, self.current_end_item):
            if x < len(self.item_list):
                item = self.item_list[x]
                item.set_size([self.size[0] - self.spacing * 2, (self.size[1] - (self.spacing * self.max_items)) / self.max_items])
                item.update()
                item.draw(surface, [self.pos[0] + self.spacing, self.position])
                self.position += self.item_height + self.spacing
                
    def scroll_list(self, index):
        if self.current_item + index >= 0 and self.current_item + index < len(self.item_list):
            self.current_item += index
            self.current_end_item = self.current_item + self.max_items
            
    def add_item(self, item):
        self.item_list.append(item)
        return item
        
    def remove_item(self, item):
        if item in self.item_list:
            self.item_list.remove(item)
        else:
            print "not in list"
        return item
        
    def set_list(self, list):
        self.item_list = list
        return list
        
    def set_spacing(self, space):
        self.spacing = space
        return space
        
    def set_max_items(self, items):
        self.max_items = items
        return items
        
    def get_item_list(self):
        return self.item_list
        
    def get_spacing(self):
        return self.spacing
        
    def get_max_items(self):
        return self.max_items
        
    def get_item_height(self):
        return self.item_height
        
    def get_position(self):
        return self.position
        
    def get_current_item(self):
        return self.current_item
        
    def clear_list(self):
        self.item_list = []