import pygame
import random

from gameObject import gameObject
from Bullet import Bullet
from Loading_Bar import Loading_Bar

Updates_per_second = 60

class Person(gameObject):
    def __init__(self, pos, size, arm_height, image_list, weapon, health, level, link=[]):
        super(Person, self).__init__(pos, size, (0,0,0), True, link)
        self.half_size = [self.size[0] / 2, self.size[1] / 2]
        self.half_arm_height = arm_height / 2
        self.arm_height = arm_height
        self.image_list = image_list
        self.image = image_list[0]
        self.equipped_primary_weapon = weapon
        self.max_health = health
        self.current_health = health
        self.health_percentage = (self.current_health / float(self.max_health)) * 100
        self.direction = 1
        self.crouching = False
        self.shooting = False
        self.level = level
        self.jumpstacks = 1
        
        #Gravity Constant
        self.gravity = 0.5
        
        #Lists that the person object keeps track of
        self.armor_list = []
        self.loading_bars = []
        
    def update(self):
        super(Person, self).update()
        if self.show:
            self.health_percentage = (self.current_health / float(self.max_health)) * 100
            
            self.vel[1] += self.gravity
            
            if self.vel[0] > 0:
                self.direction = 1
            elif self.vel[0] < 0:
                self.direction = -1
                
            if self.direction > 0 and self.crouching:
                self.image = self.image_list[2]
            elif self.direction > 0:
                self.image = self.image_list[0]
            elif self.direction < 0 and self.crouching:
                self.image = self.image_list[3]
            else:
                self.image = self.image_list[1]
                
            if self.crouching:
                self.size[1] = self.half_size[1]
                self.arm_height = self.half_arm_height + 5
            else:
                self.size[1] = self.half_size[1] * 2
                self.arm_height = self.half_arm_height * 2
                
            self.shoot()
                
    def draw(self, surface):
        if self.show:
            surface.blit(self.image, self.pos)
            
        for bar in self.loading_bars:
            bar.set_pos([self.pos[0] - 20, self.pos[1] - 30])
            bar.update()
            bar.draw(surface)
           
        pos = self.pos 
        if self.direction > 0:
            pos = [self.pos[0] + self.size[0], self.pos[1] + self.arm_height]
            self.equipped_primary_weapon.set_direction(1)
        else:
            pos = [self.pos[0] - self.equipped_primary_weapon.get_size()[0], self.pos[1] + self.arm_height]
            self.equipped_primary_weapon.set_direction(-1)
            
        self.equipped_primary_weapon.update()
        self.equipped_primary_weapon.draw(surface, pos)
        
        #Reload Gun if 0 ammo
        if self.equipped_primary_weapon.get_current_ammo() < 1:
            self.force_reload()
        
    def shoot(self):
        #Test if should be shooting
        if self.shooting and not self.equipped_primary_weapon.get_reloading():
            weapon_bullets_per_update = 3600 / int(self.equipped_primary_weapon.get_firerate())
            start_pos = self.pos
            
            if self.direction > 0:
                start_pos = [self.pos[0] + self.size[0] + self.equipped_primary_weapon.get_size()[0], self.pos[1] + self.arm_height]
            else:
                start_pos = [self.pos[0] - self.equipped_primary_weapon.get_size()[0] - 20, self.pos[1] + self.arm_height]
            #Test for which type of weapon: 0 == SMG, 1 == Assault Rifle, 2 == LMG, 3 == Shotgun, 4 == Sniper, 5 == Pistol
            if self.equipped_primary_weapon.get_type() == 0 or self.equipped_primary_weapon.get_type() == 1 or self.equipped_primary_weapon.get_type() == 2:
                if self.loop_count % weapon_bullets_per_update < 1:
                    bullet = Bullet(start_pos, [15,3], (0,0,0), [15 * self.direction, 0.001], self.equipped_primary_weapon.get_damage())
                    self.equipped_primary_weapon.add_bullet(bullet)
                    self.equipped_primary_weapon.remove_current_ammo(1)
                    
            elif self.equipped_primary_weapon.get_type() == 4 or self.equipped_primary_weapon.get_type() == 5:
                if not self.equipped_primary_weapon.get_shot():
                    bullet = Bullet(start_pos, [20,3], (0,0,0), [30 * self.direction, 0.001], self.equipped_primary_weapon.get_damage())
                    self.equipped_primary_weapon.add_bullet(bullet)
                    self.equipped_primary_weapon.set_shot(True)
                    self.equipped_primary_weapon.remove_current_ammo(1)
            
            elif self.equipped_primary_weapon.get_type() == 3:
                if not self.equipped_primary_weapon.get_shot():
                    for x in range(0,10):
                        bullet = Bullet([start_pos[0], start_pos[1]], [15,3], (0,0,0), [15 * self.direction, x - 5], self.equipped_primary_weapon.get_damage())
                        self.equipped_primary_weapon.add_bullet(bullet)
                    self.equipped_primary_weapon.set_shot(True)
                    self.equipped_primary_weapon.remove_current_ammo(1)
                    
    def jump(self, height):
        if self.jumpstacks > 0:
            self.vel[1] = -height
            self.jumpstacks -= 1
                    
    def add_healthbar(self):
        health_bar = Loading_Bar([self.pos[0] - 20, self.pos[1] - 30], [100, 10], (200,0,0), (0,0,0), 128, 200, 2, True, [], [lambda: self.get_current_health(), lambda: self.get_max_health()])
        self.loading_bars = [health_bar]
         
    def set_image_list(self, list):
        if len(list) == 4:
            self.image_list = list
        else:
            print "requires more images"
        return list
        
    def clone(self):
        return Person([self.pos[0], self.pos[1]], [self.size[0], self.size[1]], self.arm_height, self.image_list, self.equipped_primary_weapon.clone(), self.max_health, self.level, self.link)
        
    def set_equipped_primary_weapon(self, weapon):
        self.equipped_primary_weapon = weapon
        return weapon
        
    def set_max_health(self, health):
        self.max_health = health
        return health
        
    def set_current_health(self, health):
        self.current_health = health
        return health
        
    def set_gravity(self, magnitude):
        self.gravity = magnitude    
        return magnitude
        
    def set_crouching(self, crouch_bool):
        self.crouching = crouch_bool        
        return crouch_bool
        
    def set_shooting(self, shooting_bool):
        self.shooting = shooting_bool
        return shooting_bool
        
    def set_level(self, level):
        self.level = level
        return level
        
    def add_armor(self, armor_object):
        self.armor_list.append(armor_object)
        return armor_object
        
    def set_armor_list(self, list):
        self.armor_list = list
        return list
        
    def set_jumpstacks(self, amount):
        self.jumpstacks = amount
        return amount
        
    def get_image_list(self):
        return self.image_list
        
    def get_current_image(self):
        return self.image
        
    def get_equipped_primary_weapon(self):
        return self.equipped_primary_weapon
        
    def get_max_health(self):
        return self.max_health
        
    def get_current_health(self):
        return self.current_health
        
    def get_health_percentage(self):
        return self.health_percentage
        
    def get_gravity(self):
        return self.gravity
        
    def get_direction(self):
        return self.direction
        
    def get_crouching(self):
        return self.crouching
        
    def get_shooting(self):
        return self.shooting
        
    def get_armor_list(self):
        return self.armor_list
        
    def get_level(self):
        return self.level
        
    def get_jumpstacks(self):
        return self.jumpstacks
        
    def remove_health(self, amount):
        self.current_health -= amount
        return amount
        
    def force_reload(self):
        if self.equipped_primary_weapon.get_current_ammo() < self.equipped_primary_weapon.get_clip_size():
            self.equipped_primary_weapon.set_reloading(True)
            
    def add_jumpstacks(self, amount=1):
        self.jumpstacks += amount
        return amount