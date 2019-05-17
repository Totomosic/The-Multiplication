import pygame
from Person import Person
from Weapon import Weapon

class Player(Person):
    def __init__(self, pos, size, image_list, weapon, health, level=0, link=[]):
        super(Player, self).__init__(pos, size, image_list, weapon, health, level, link)
        self.xp = 100
        self.xplist = []
        self.attributes = [0,0,0]
        
        self.name = "Totomosic"
        
        self.inventory_capacity = 30
        self.inventory_list = []
        self.update_inv = True
        
        self.extracted_list = []
        
        self.selected_weapon = self.equipped_primary_weapon
        
        for x in range(0,30):
            self.xplist.append(100 * (1.5 ** x))
            
    def update(self):
        super(Player, self).update()
        
        if self.current_health + 10 <= self.max_health:
            self.current_health += 10
        
    def get_xp(self):
        return self.xp
        
    def get_xp_list(self):
        return self.xplist
        
    def get_attributes(self):
        return self.attributes
        
    def get_selected_weapon(self):
        return self.selected_weapon
        
    def get_inventory_capacity(self):
        return self.inventory_capacity
        
    def get_inventory_list(self):
        return self.inventory_list
        
    def get_name(self):
        return self.name
        
    def get_update_inv(self):
        return self.update_inv
        
    def get_extracted_items(self):
        return self.extracted_list
        
    def set_inventory_list(self, list):
        self.inventory_list = list
        self.update_inv = True
        return list
        
    def set_selected_weapon(self, weapon):
        self.selected_weapon = weapon
        return weapon
        
    def set_inventory_capacity(self, cap):
        self.inventory_capacity = cap
        
    def set_xp(self, xp):
        self.xp = xp
        return xp
        
    def set_attributes(self, attribute_list):
        self.attributes = attribute_list
        
    def set_update_inv(self, bool):
        self.update_inv = bool
        
    def add_xp(self, amount):
        self.xp += amount
        return amount
        
    def add_inventory_item(self, item):
        self.inventory_list.append(item)
        self.update_inv = True
        return item
        
    def add_extracted_item(self, item):
        self.extracted_list.append(item)
        return item
        
    def remove_extracted_item(self, item):
        if item in self.extracted_list:
            self.extracted_list.remove(item)
        else:   
            print "not in list"
        return item
        
    def remove_inventory_item(self, item):
        if item in self.inventory_list:
            self.inventory_list.remove(item)
            self.update_inv = True
        else:
            print "not in list"
        return item