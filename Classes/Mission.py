import pygame
from Timer import Timer
from Text import Text

class Mission:
    def __init__(self, name, desc, rec_level, xp, player):
        self.name = name
        self.desc = desc
        self.rec_level = rec_level
        self.player = player
        self.xp = xp
        
        self.color = (0,0,0)
        
        self.wave_timer = Timer(5, [lambda: self.start_next_wave()], True)
        self.end_text = Text(self.name + " Completed!", [540, 200], (0,0,0), 50, "impact", True, 180)
        
        self.current_wave = 0
        self.active = False
        self.completed = False
        self.given_xp = False
        
        self.enemy_list = []
        self.enemy_clone_list = []
        self.cover_list = []
        
        if self.rec_level > 25: 
            self.color = (200,0,0)
        elif self.rec_level > 20:
            self.color = (200,200,0)
        elif self.rec_level > 15:     
            self.color = (200,200,100)
        elif self.rec_level > 10:
            self.color = (0,0,200)
        elif self.rec_level > 5:
            self.color = (0,200,0)
        else:
            self.color = (0,200,200)  
        
    def update(self):
        if self.active:
            self.wave_timer.update()
            isEnemies = False
            for enemy in self.enemy_clone_list:
                enemy[0].add_healthbar()
                if enemy[1] == self.current_wave:
                    enemy[0].update()
                    enemy[0].AI(self.cover_list, self.player)
                    isEnemies = True
            if not isEnemies:  
                self.wave_timer.start()
                
            if len(self.enemy_list) > 0 and len(self.enemy_clone_list) <= 0:
                self.completed = True
            
            if self.completed and not self.given_xp:
                self.given_xp = True
                self.player.add_xp(self.xp)
                
            if len(self.enemy_clone_list) == 0 and len(self.enemy_list) > 0:
                self.deactivate_mission()  
                
        if self.rec_level > 25: 
            self.color = (200,0,0)
        elif self.rec_level > 20:
            self.color = (200,200,0)
        elif self.rec_level > 15:     
            self.color = (200,200,100)
        elif self.rec_level > 10:
            self.color = (0,0,200)
        elif self.rec_level > 5:
            self.color = (0,200,0)
        else:
            self.color = (0,200,200)  
          
    def draw(self, surface):
        if self.active:
            for enemy in self.enemy_clone_list:
                if enemy[1] == self.current_wave:
                    enemy[0].draw(surface)
                    
            for cover in self.cover_list:
                cover.update()
                cover.draw(surface)
             
        if self.completed and self.end_text.get_age() < self.end_text.get_lifespan():
            self.end_text.update()
            self.end_text.draw(surface)
               
    def start_next_wave(self):
        self.current_wave += 1

    def add_enemy(self, enemy, wave):
        self.enemy_list.append([enemy, wave])
        
    def add_cover(self, cover):
        self.cover_list.append(cover)
        
    def get_enemies(self):
        return_list = []
        for enemy in self.enemy_clone_list:
            if enemy[1] == self.current_wave:
                return_list.append(enemy[0])
        return return_list
        
    def get_covers(self):
        return self.cover_list
        
    def get_wave(self):
        return self.current_wave
        
    def get_name(self):
        return self.name
        
    def get_desc(self):
        return self.desc
        
    def get_color(self):
        return self.color
        
    def get_level(self):
        return self.rec_level
        
    def get_active(self):
        return self.active
        
    def set_wave(self, wave):
        self.current_wave = wave
        return wave
        
    def activate_mission(self):
        self.current_wave = 0
        self.wave_timer.stop()
        self.wave_timer.reset()
        for enemy in self.enemy_list:
            self.enemy_clone_list.append([enemy[0].clone(), enemy[1]])
        self.active = True
        
    def deactivate_mission(self):
        self.active = False
        self.enemy_clone_list = []
        
    def remove_enemy(self, enemy):
        for list in self.enemy_clone_list:
            if enemy in list:
                self.enemy_clone_list.remove(list)
            else:
                print "not in list"