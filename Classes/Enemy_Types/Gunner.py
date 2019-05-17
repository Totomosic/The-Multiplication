import pygame
import random
from Classes.Enemy import Enemy

class Gunner(Enemy):
    def AI(self, obstacle_list, player):
        selected_obstacle = player
        super(Gunner, self).AI(obstacle_list, player)
        if len(obstacle_list) > 0 and not self.update_pos:
            selected_obstacle = obstacle_list[random.randrange(0, len(obstacle_list))]
            if player.get_pos()[0] > self.pos[0]:
                self.destination = [selected_obstacle.get_pos()[0] - self.size[0] - 5, self.pos[1]]
            else:
                self.destination = [selected_obstacle.get_pos()[0] + selected_obstacle.get_size()[0] + 5, self.pos[1]]
            self.update_pos = True
                
        if abs(player.get_pos()[0] - self.pos[0]) < selected_obstacle.get_size()[0] and len(obstacle_list) > 0 and self.reached_destination:
            self.update_pos = False
        
    def clone(self):
        return Gunner([self.pos[0], self.pos[1]], [self.size[0], self.size[1]], self.arm_height, self.image_list, self.equipped_primary_weapon.clone(), self.max_health, self.level, self.shield, self.isBoss, self.name)