import pygame
from Surface import Surface

class Menu(Surface):
    def __init__(self, pos, size, color, alpha, show=True, link=[]):
        super(Menu, self).__init__(pos, size, color, alpha, show, link)
        self.buttons = []
        self.texts = []
        self.lists = []
        self.surfaces = []
        self.menus = []
        
        self.selected_menu = self
       
    def update(self):
        super(Menu, self).update()
                        
    def draw(self, surface):
        if self.selected_menu == self:
            super(Menu, self).draw(surface)
            
            if self.show:
                for item in self.buttons:
                    if self.show:  
                        item.set_show(True)
                    else:
                        item.set_show(False)
                    item.update()
                    item.draw(surface)
                    item.set_pos([self.pos[0] + item.get_displacement()[0], self.pos[1] + item.get_displacement()[1]])
                    
                for item in self.texts:
                    if self.show:  
                        item.set_show(True)
                    else:
                        item.set_show(False)
                    item.update()
                    item.draw(surface)
                    item.set_pos([self.pos[0] + item.get_displacement()[0], self.pos[1] + item.get_displacement()[1]])
                    
                for item in self.lists:
                    if self.show:  
                        item.set_show(True)
                    else:
                        item.set_show(False)
                    item.update()
                    item.draw(surface)
                    item.set_pos([self.pos[0] + item.get_displacement()[0], self.pos[1] + item.get_displacement()[1]])
                    
                for item in self.surfaces:
                    if self.show:  
                        item.set_show(True)
                    else:
                        item.set_show(False)
                    item.update()
                    item.draw(surface)
                    item.set_pos([self.pos[0] + item.get_displacement()[0], self.pos[1] + item.get_displacement()[1]])
                    
        for menu in self.menus:
            if menu == self.selected_menu:
                menu.set_show(True)
                menu.update()
                menu.draw(surface)
            else:
                menu.set_show(False)                
                for button in menu.get_buttons():
                    button.set_updatable(False)
            
    def add_button(self, button):
        self.buttons.append(button)
        button.set_displacement(button.get_pos())
        button.set_pos([button.get_pos()[0] + self.pos[0], button.get_pos()[1] + self.pos[1]])        
        return button
      
    def add_text(self, text):
        self.texts.append(text)
        text.set_displacement(text.get_pos())
        text.set_pos([text.get_pos()[0] + self.pos[0], text.get_pos()[1] + self.pos[1]])        
        return text
        
    def add_list(self, list):
        self.lists.append(list)
        list.set_displacement(list.get_pos())
        list.set_pos([list.get_pos()[0] + self.pos[0], list.get_pos()[1] + self.pos[1]])        
        return list
        
    def add_surface(self, surface):
        self.surfaces.append(surface)
        surface.set_displacement(surface.get_pos())
        surface.set_pos([surface.get_pos()[0] + self.pos[0], surface.get_pos()[1] + self.pos[1]])        
        return surface
        
    def add_menu(self, menu):
        self.menus.append(menu)
        menu.set_displacement(menu.get_pos())
        menu.set_pos([menu.get_pos()[0] + self.pos[0], menu.get_pos()[1] + self.pos[1]])
        return menu
        
    def get_buttons(self):
        return self.buttons
        
    def get_texts(self):
        return self.texts
        
    def get_lists(self):
        return self.lists
        
    def get_surfaces(self):
        return self.surfaces
        
    def get_menus(self):
        return self.menus
        
    def get_selected_menu(self):
        return self.selected_menu
        
    def set_selected_menu(self, menu):
        if menu in self.menus or menu == self:
            self.selected_menu = menu
        else:
            print "not a known menu"
        return menu