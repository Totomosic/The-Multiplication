import pygame

Updates_per_second = 60

class Timer:
    def __init__(self, seconds, functions, reset_after_finished=False):
        self.current_time = 0
        self.max_time = seconds * Updates_per_second
        self.functions = functions
        self.should_stop = reset_after_finished
        
        self.running = False
        
    def update(self):
        if self.running:
            self.current_time += 1
            
            if self.current_time >= self.max_time:
                for function in self.functions:
                    function()
                if self.should_stop:
                    self.stop()
                    self.reset()
                return True
        return False
        
    def draw(self, surface):
        pass
        
    def start(self):
        self.running = True
      
    def stop(self):
        self.running = False
        
    def reset(self, stop=False):
        if stop:
            self.stop()
            self.current_time = 0
        else:
            self.current_time = 0
            
    def get_current_time(self):
        return self.current_time
        
    def get_max_time(self):
        return self.max_time
        
    def get_seconds(self):
        return self.max_time / 60
        
    def get_status(self):
        return self.running
        
    def set_seconds(self, seconds):
        self.max_time = seconds * 60
        
    def add_current_time(self, time):
        self.current_time += time
        
    def get_time_remaining(self):
        return str((self.max_time - self.current_time) / (60 * 60 * Updates_per_second) / 10 % 6) + str((self.max_time - self.current_time) / (60 * 60 * Updates_per_second) % 10) + ":" + str((self.max_time - self.current_time) / (60 * Updates_per_second) / 10 % 6) + str((self.max_time - self.current_time) / (60 * Updates_per_second) % 10) + ":" + str((self.max_time - self.current_time) / (Updates_per_second) / 10 % 6) + str((self.max_time - self.current_time) / (Updates_per_second) % 10) + "." + str((self.max_time - self.current_time) % 6) + str((self.max_time - self.current_time) % 10)