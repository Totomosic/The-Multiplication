import pygame
import random
from Classes.Enemy import Enemy

class Marksman(Enemy):    
    def AI(self, obstacle_list, player):
        super(Marksman, self).AI(obstacle_list, player)
        if len(obstacle_list) > 0 and not self.update_pos:
            selected_obstacle = obstacle_list[0]
            distance = abs(selected_obstacle.get_pos()[0] - player.get_pos()[0])
            
            for obstacle in obstacle_list:
                obst_dist = abs(obstacle.get_pos()[0] - player.get_pos()[0])
                if obst_dist > distance:
                    selected_obstacle = obstacle
            
            if player.get_pos()[0] < self.pos[0]:                   
                self.destination = [selected_obstacle.get_pos()[0] + selected_obstacle.get_size()[0] + 5, self.pos[1]]
            else:
                self.destination = [selected_obstacle.get_pos()[0] - self.size[0] - 5, self.pos[1]]
            self.update_pos = True
            
        if len(obstacle_list) > 0:
            selected_obstacle = obstacle_list[0]
            distance = abs(selected_obstacle.get_pos()[0] - self.pos[0])                
            for obstacle in obstacle_list:
                obst_dist = abs(obstacle.get_pos()[0] - self.pos[0])
                if obst_dist < distance:
                    selected_obstacle = obstacle    
            if abs(player.get_pos()[0] - self.pos[0]) < selected_obstacle.get_size()[0]:
                self.update_pos = False
            
    def clone(self):
        return Marksman([self.pos[0], self.pos[1]], [self.size[0], self.size[1]], self.arm_height, self.image_list, self.equipped_primary_weapon.clone(), self.max_health, self.level, self.shield, self.isBoss, self.name)