import pygame
from Button import Button
from Text import Text
from Surface import Surface

class List_Item(Button):
    def __init__(self, id, list_block, color, active_color, alpha, functions, item):
        if len(functions) > 0:
            super(List_Item, self).__init__([list_block.get_pos()[0] + list_block.get_spacing(), list_block.get_pos()[1]], [list_block.get_size()[0] - list_block.get_spacing() * 2, list_block.get_item_height()], color, active_color, alpha, [lambda: functions[0](item)], True, [list_block])
        else:
            super(List_Item, self).__init__([list_block.get_pos()[0] + list_block.get_spacing(), list_block.get_pos()[1]], [list_block.get_size()[0] - list_block.get_spacing() * 2, list_block.get_item_height()], color, active_color, alpha, [], True, [list_block])
        self.list_block = list_block
        self.id = id
        self.item = item
        self.texts = []
        self.surfaces = []
    
    def update(self):
        self.updatable = True
        super(List_Item, self).update()
        my_index = self.list_block.get_item_list().index(self) - self.list_block.get_current_item()
        self.pos = [self.list_block.get_pos()[0] + self.list_block.get_spacing(), self.list_block.get_pos()[1] + self.list_block.get_spacing() + self.list_block.get_item_height() * my_index]
    
    def draw(self, surface, pos):
        surface.blit(self.surface, pos)
        for text in self.texts:
            text.set_pos([pos[0] + text.get_displacement()[0], pos[1] + text.get_displacement()[1]])
            text.update()
            text.draw(surface)    
            
        for surfaces in self.surfaces:
            surfaces.set_pos([pos[0] + surfaces.get_displacement()[0], pos[1] + surfaces.get_displacement()[1]])
            surfaces.update()
            surfaces.draw(surface)       
        
    def add_text(self, text, rel_pos, color, size, font, show=True, lifespan=False, link=[], var_link=[]):
        text = Text(str(text), rel_pos, color, size, font, show, lifespan, link, var_link)
        text.set_displacement(rel_pos)
        self.texts.append(text)
        return text
        
    def add_mod_slots(self):
        x_pos = 20
        for slot in range(0,self.item.get_mod_slots()):            
            if len(self.item.get_mod_list()) > slot:
                mod_rect = Surface([x_pos, self.size[1] - 15], [20,5], self.item.get_mod_list()[slot].get_color(), 128)
            else:
                mod_rect = Surface([x_pos, self.size[1] - 15], [20,5], (0,0,0), 128)
            mod_rect.set_displacement([x_pos, self.size[1] - 15])
            x_pos += 25
            self.surfaces.append(mod_rect)
        
    def get_id(self):
        return self.id
        
    def set_id(self, id):
        self.id = id