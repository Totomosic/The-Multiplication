import pygame
from Surface import Surface

class Drop(Surface):
    def __init__(self, pos, size, color, alpha, items, lifespan):
        super(Drop, self).__init__(pos, size, color, alpha)
        self.items = items
        self.lifespan = lifespan
        self.age = 0
        
    def update(self):
        super(Drop, self).update()
        self.age += 1
        
        if self.age >= self.lifespan:
            return True
        return False
        
    def get_items(self):
        return self.items
        
    def get_age(self):
        return self.age
        
    def get_lifespan(self):
        return self.lifespan
        
    def set_items(self, list):
        self.items = list
        return list
        
    def set_age(self, age):
        self.age = age
        return age
        
    def set_lifespan(self, life):
        self.lifespan = life
        return life
        
    def add_item(self, item):
        self.items.append(item)
        return item
        
    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
        else:
            print "not in list"
        return item