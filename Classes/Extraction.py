import pygame

from Timer import Timer
from gameObject import gameObject
from Loading_Bar import Loading_Bar
from Surface import Surface
from Text import Text

class Extraction:
    def __init__(self, player, extract_pos, display_size, delay_time, extraction_time):
        self.pos = extract_pos
        self.display_size = display_size
        
        self.helicopter_image_reverse = pygame.image.load("Art/Helicopter.png")
        self.helicopter_image = pygame.transform.flip(self.helicopter_image_reverse, True, False)
        self.helicopter_image_size = [80,50]
        self.helicopter_direction = 1
        self.helicopter_pos = [0, display_size[1] * 0.1]
        self.vel = [2 * self.helicopter_direction,0]
        
        self.delay_timer = Timer(delay_time, [lambda: self.start_extraction()], True)
        self.extraction_timer = Timer(extraction_time, [lambda: self.stop_extraction()], True)
        self.reached_dest = False
        
        self.time_remaining_text = Text("Extraction Started by " + player.get_name(), [display_size[0] / 2, display_size[1] * 0.3], (0,0,0), 30, "impact", True, False, [], False, False)
        self.time_left_text = Text("Extraction Leaving in: ", [display_size[0] / 2, display_size[1] * 0.3], (0,0,0), 30, "impact", True, False, [], lambda: self.extraction_timer.get_time_remaining(), False)
        
        self.started = False
        self.finished = False
        
        self.line_pos = [self.helicopter_pos[0] + self.helicopter_image_size[0] / 2, self.helicopter_pos[1] + self.helicopter_image_size[1]]
        self.end_line_pos = self.line_pos[1]
        
    def update(self):
        self.delay_timer.update()
        self.extraction_timer.update()
    
        self.delay_timer.start()  
        
        if self.delay_timer.get_current_time() >= 180:
            self.time_remaining_text.set_original_text("Extraction Arriving in: ")       
            self.time_remaining_text.set_var_link(lambda: self.delay_timer.get_time_remaining()) 
            
            if self.delay_timer.get_current_time() + 10 * 60 >= self.delay_timer.get_max_time():
                self.time_remaining_text.set_color((255,0,0)) 
                
            if self.extraction_timer.get_current_time() + 10 * 60 >= self.delay_timer.get_max_time():
                self.time_left_text.set_color((255,0,0)) 
            
            if self.delay_timer.get_current_time() > 600:
                self.time_remaining_text.set_text_size(20)
                self.time_remaining_text.set_pos([self.display_size[0] * 0.2, self.display_size[1] * 0.04])     
        
        if self.started:
            if self.helicopter_pos[0] < self.pos[0] - 10 or self.helicopter_pos[0] > self.pos[0] + 10:
                self.helicopter_pos[0] += self.vel[0]
                self.helicopter_pos[1] += self.vel[1]
            else:
                self.reached_dest = True
             
        if self.helicopter_pos[0] > self.display_size[0]:
            return True
        else:
            return False
    
    def draw(self, surface):
        if not self.started:
            self.time_remaining_text.update()
            self.time_remaining_text.draw(surface)
    
        if self.started:
            surface.blit(self.helicopter_image, self.helicopter_pos)

            pygame.draw.line(surface, (0,0,0), self.line_pos, [self.line_pos[0], self.end_line_pos], 5)
            
            if self.end_line_pos < self.display_size[1] - 200 and self.reached_dest and not self.finished:
                self.end_line_pos += 3
            elif self.reached_dest and not self.finished:
                self.extraction_timer.start()
                self.time_left_text.update()
                self.time_left_text.draw(surface) 
                
        self.line_pos[0] = self.helicopter_pos[0] + self.helicopter_image_size[0] / 2     
        if self.finished:
            
            pygame.draw.line(surface, (0,0,0), self.line_pos, [self.line_pos[0], self.end_line_pos], 5)
            
            if self.end_line_pos > self.line_pos[1]:
                self.end_line_pos -= 3              
            else:
                self.helicopter_pos[0] += self.vel[0]
                self.helicopter_pos[1] += self.vel[1]
                
    def start_extraction(self):
        self.started = True
        
    def stop_extraction(self):
        self.finished = True
        
    def get_pos(self):
        return [self.line_pos[0], self.end_line_pos]        