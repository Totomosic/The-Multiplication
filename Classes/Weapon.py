import pygame
from Item import Item

Updates_per_second = 60

class Weapon(Item):
    def __init__(self, name, desc, type, rank, image, image_size, clip_size, total, damage, firerate, reload_time, level, crit_chance=0, crit_multiplier=1.4, head_shot_multiplier=2):
        super(Weapon, self).__init__(name, desc, type, rank, image, image_size, level)
        self.weapon_type = type
        self.damage = damage
        self.original_damage = damage
        self.firerate = firerate
        self.original_firerate = firerate
        self.reloading = False
        self.reload_time = reload_time
        self.reload_timer = 0
        self.image_size = image_size
        self.current_ammo = clip_size
        self.clip_size = clip_size
        self.original_clip_size = clip_size
        self.crit_chance = crit_chance
        self.crit_mult = crit_multiplier
        self.head_shot_mul = head_shot_multiplier
        self.total = total - self.current_ammo
        self.shot_cooldown = self.reload_time / 3
        self.shot = False
        
        self.shot_count = 1
        if self.type == 3:
            self.shot_count = 10
        
        self.dps = (self.damage * (1 + self.crit_chance * (self.crit_mult / 100.0))) * self.shot_count * (self.firerate / 60)
        
        self.bullet_list = []
        
    def update(self):
        super(Weapon, self).update()
        
        self.dps = (self.damage * (1 + self.crit_chance * (self.crit_mult / 100.0))) * self.shot_count * (self.firerate / 60)
        
        if self.reloading:
            self.reload_timer += 1
            if self.reload_timer >= self.reload_time * Updates_per_second:
                self.reloading = False
                if self.total - self.clip_size - self.current_ammo >= 0:
                    self.total += self.remove_current_ammo(-(self.clip_size - self.current_ammo))
                else:
                    self.current_ammo = self.total
                    self.total = 0
                self.reload_timer = 0
                
        if self.type > 2 and self.shot:
            self.shot_cooldown += 1
            if self.shot_cooldown >= self.reload_time / 2 * Updates_per_second:
                self.shot_cooldown = 0
                self.shot = False
                
        if self.type == 3:
            for bullet in self.bullet_list:
                bullet.set_damage_decay(0.95)
        
    def draw(self, surface, pos):
        super(Weapon, self).draw(surface, pos)
        for bullet in self.bullet_list:
            bullet.update()
            bullet.draw(surface)
            
            if bullet.get_damage() < self.damage / 3:
                self.bullet_list.remove(bullet)
                
    def clone(self):
        return Weapon(self.name, self.desc, self.type, self.rank, self.image, self.image_size, self.clip_size, self.total, self.damage, self.firerate, self.reload_time, self.level, self.crit_chance, self.crit_mult, self.head_shot_mul)
            
    def get_weapon_type(self):
        return self.weapon_type
        
    def get_damage(self):
        return self.damage
        
    def get_firerate(self):
        return self.firerate
        
    def get_bullet_list(self):
        return self.bullet_list
     
    def get_reloading(self):
        return self.reloading
        
    def get_reloading_time(self):
        return self.reloading_time
        
    def get_current_ammo(self):
        return self.current_ammo
        
    def get_total_ammo(self):
        return self.total
        
    def get_clip_size(self):
        return self.clip_size
        
    def get_shot(self):
        return self.shot
        
    def get_dps(self):
        return int(self.dps)
        
    def get_crit_chance(self):
        return self.crit_chance
        
    def get_crit_mult(self):
        return self.crit_mult
        
    def get_headshot_mult(self):
        return self.head_shot_mul
        
    def get_original_damage(self):
        return self.original_damage
        
    def get_original_firerate(self):
        return self.original_firerate
        
    def get_original_clip_size(self):
        return self.original_clip_size
                
    def set_weapon_type(self, type):
        self.weapon_type = type
        return type
        
    def set_damage(self, damage):
        self.damage = damage
        return damage
        
    def set_firerate(self, firerate):
        self.firerate = firerate
        return firerate
        
    def set_reloading(self, bool):
        self.reloading = bool
        return bool
        
    def set_reloading_time(self, time):
        self.reloading_time = time
        return time
        
    def set_current_ammo(self, amount):
        self.current_ammo = amount
        return amount
        
    def set_total(self, amount):
        self.total = amount
        return amount
        
    def set_clip_size(self, amount):
        self.clip_size = clip_size
        return amount
        
    def set_shot(self, bool):
        self.shot = bool
        return bool
        
    def set_crit_chance(self, chance):
        self.crit_chance = chance
        return chance
        
    def set_crit_mult(self, scale):
        self.crit_mult = scale
        return scale
        
    def set_headshot_mult(self, scale):
        self.head_shot_mul = scale
        return scale
        
    def set_original_damage(self, damage):
        self.original_damage = damage
        return damage
        
    def set_original_firerate(self, rate):
        self.original_firerate = rate
        return rate
        
    def set_original_clip_size(self, size):
        self.original_clip_size = size
        return size
        
    def remove_current_ammo(self, amount):
        self.current_ammo -= amount
        return amount
        
    def add_bullet(self, bul_obj):
        self.bullet_list.append(bul_obj)
        return bul_obj
        
    def remove_bullet(self, bul_obj):
        if bul_obj in self.bullet_list:
            self.bullet_list.remove(bul_obj)
        else:
            print "bullet not in list"
        return bul_obj