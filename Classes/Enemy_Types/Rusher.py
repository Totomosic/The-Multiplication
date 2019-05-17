import pygame
import random
from Classes.Enemy import Enemy

class Rusher(Enemy):        
    def AI(self, obstacle_list, player):
        super(Rusher, self).AI(obstacle_list, player)
        if player.get_pos()[0] > self.pos[0] and self.loop_count % 180 == 0:
            self.destination = [player.get_pos()[0] - random.randrange(0,100), self.pos[1]]
        elif self.loop_count % random.randrange(60,240) == 0:
            self.destination = [player.get_pos()[0] + player.get_size()[0] + random.randrange(0, 100), self.pos[1]]    
 
    def clone(self):
        return Rusher([self.pos[0], self.pos[1]], [self.size[0], self.size[1]], self.arm_height, self.image_list, self.equipped_primary_weapon.clone(), self.max_health, self.level, self.shield, self.isBoss, self.name)