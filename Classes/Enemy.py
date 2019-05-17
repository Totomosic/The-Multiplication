import pygame
import random
from Person import Person
from Loading_Bar import Loading_Bar
from Text import Text

class Enemy(Person):
    def __init__(self, pos, size, arm_height, image_list, weapon, health, level, shield=0, isBoss=False, name=False):
        super(Enemy, self).__init__(pos, size, arm_height, image_list, weapon, health, level)
        self.direction = -1
        self.destination = self.pos
        self.reached_destination = False
        self.max_shield = shield
        self.shield = shield
        self.isBoss = isBoss
        self.name = name
        
        if self.name:
            self.name_text = Text(self.name, [self.pos[0] + self.size[0] / 2, self.size[1] - 30], (0,0,0), 20, "tahoma")

        self.speed = 2
        
        self.update_pos = False
        
    def draw(self, surface):
        super(Enemy, self).draw(surface)

        if self.name:
            self.name_text.set_pos([self.pos[0] + self.size[0] / 2, self.pos[1] - 40])
            self.name_text.update()
            self.name_text.draw(surface) 
        
    def AI(self, obstacle_list, player):           
        if not self.reached_destination:
            if self.destination[0] > self.pos[0]:
                self.vel[0] = self.speed
            else:
                self.vel[0] = -self.speed
        else:
            self.vel[0] = 0
                
        if self.pos[0] > self.destination[0] - 3 and self.pos[0] < self.destination[0] + 3:
            self.reached_destination = True
        else:
            self.reached_destination = False
                    
        if self.loop_count % random.randrange(10,240) == 0:
            if player.get_pos()[0] > self.pos[0]:
                self.direction = 1
            else:
                self.direction = -1
                
        if self.yCollision([player.get_pos()[0], player.get_pos()[1], player.get_size()[0], player.get_size()[1]]):
            shoot_chance = random.randrange(0,150)
            if shoot_chance == 1:
                self.shooting = True
                
        if random.randrange(0,100) == 1:
            self.shooting = False
                        
        if not self.reached_destination:
            for obstacle in obstacle_list:
                if self.collision([obstacle.get_pos()[0] - 30, obstacle.get_pos()[1], obstacle.get_size()[0] + 30, obstacle.get_size()[1]]):
                    self.jump(12)      
                
    def remove_shield(self, amount):
        self.shield -= amount
        return amount
                
    def add_healthbar(self):
        color = (200,0,0)
        if self.isBoss:
            color = (255,255,0)
        health_bar = Loading_Bar([self.pos[0] - 20, self.pos[1] - 30], [100, 10], color, (0,0,0), 128, 200, 2, True, [], [lambda: self.get_current_health(), lambda: self.get_max_health()])
        self.loading_bars = [health_bar]
        if self.shield > 0:
            shield_bar = Loading_Bar([self.pos[0] - 20, self.pos[1] - 30], [100, 10], (200,200,200), (0,0,0), 10, 0, 2, True, [], [lambda: self.get_current_shield(), lambda: self.get_max_shield()])
            self.loading_bars = [health_bar, shield_bar]
      
    def get_current_shield(self):
        return self.shield
        
    def get_max_shield(self):
        return self.max_shield
        
    def remove_health(self, amount):
        damage_amount = amount
        damage_amount -= self.shield
        if damage_amount < 0:
            damage_amount = 0
        self.shield -= amount
        self.current_health -= damage_amount
        
            