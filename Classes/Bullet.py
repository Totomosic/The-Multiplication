import pygame
from gameObject import gameObject

class Bullet(gameObject):
    def __init__(self, pos, size, color, vel, damage):
        super(Bullet, self).__init__(pos, size, color, True)
        self.damage = damage
        self.damage_decay = 0.985
        self.set_vel(vel)
        
    def update(self):
        super(Bullet, self).update()
        self.damage *= self.damage_decay
        
    def get_damage(self):
        return int(self.damage)
        
    def get_damage_decay(self):
        return self.damage_decay
        
    def set_damage(self, damage):
        self.damage = damage
        return damage
        
    def set_damage_decay(self, decay):
        self.damage_decay = decay
        return decay