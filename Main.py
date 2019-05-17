import pygame
import random
import math

#Import Classes
#from Classes.class import class
from Classes.gameObject import gameObject
from Classes.Person import Person
from Classes.Surface import Surface
from Classes.Button import Button
from Classes.Text import Text
from Classes.List_Block import List_Block
from Classes.List_Item import List_Item
from Classes.Menu import Menu
from Classes.Player import Player
from Classes.Weapon import Weapon
from Classes.Loading_Bar import Loading_Bar
from Classes.Confirmation_Menu import Confirmation_Menu
from Classes.Timer import Timer
from Classes.Extraction import Extraction
from Classes.Enemy import Enemy
from Classes.Enemy_Types.Marksman import Marksman
from Classes.Enemy_Types.Rusher import Rusher
from Classes.Enemy_Types.Gunner import Gunner
from Classes.Mission import Mission
from Classes.Drop import Drop

pygame.init()

#Define Constants
WIDTH = 1080
HEIGHT = 720
BG_COLOR = (255,255,255)

Updates_per_second = 60
clock = pygame.time.Clock()

#Define Colors
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
orange = (200,165,0)
yellow = (200,200,0)
purple = (160,32,240)

#Create the frame for the game
gameDisplay = pygame.display.set_mode([WIDTH, HEIGHT], pygame.DOUBLEBUF, 32)
pygame.display.set_caption("Jordan Morrison's The Multiplication")

#Import Art and Sounds for the game
player_standing_img = pygame.image.load("Art/Player_Standing.png")
player_crouching_img = pygame.image.load("Art/Player_Crouching.png")
rioter_standing_img = pygame.image.load("Art/Rioter_Standing.png")
rioter_crouching_img = pygame.image.load("Art/Rioter_Crouching.png")
AUG_image = pygame.image.load("Art/AUG.png")
AK47_image = pygame.image.load("Art/AK47.png")
P90_image = pygame.image.load("Art/P90.png")
AWP_image = pygame.image.load("Art/AWP.png")
XM_image = pygame.image.load("Art/XM.png")
DEAGLE_image = pygame.image.load("Art/Deagle.png")

#Reverse Images
player_standing_img_reverse = pygame.transform.flip(player_standing_img, True, False)
player_crouching_img_reverse = pygame.transform.flip(player_crouching_img, True, False)
rioter_standing_img_reverse = pygame.transform.flip(rioter_standing_img, True, False)
rioter_crouching_img_reverse = pygame.transform.flip(rioter_crouching_img, True, False)
AUG_image_reverse = pygame.transform.flip(AUG_image, True, False)
AK47_image_reverse = pygame.transform.flip(AK47_image, True, False)
P90_image_reverse = pygame.transform.flip(P90_image, True, False)
AWP_image_reverse = pygame.transform.flip(AWP_image, True, False)
XM_image_reverse = pygame.transform.flip(XM_image, True, False)
DEAGLE_image_reverse = pygame.transform.flip(DEAGLE_image, True, False)

#Object Groups
menu_group = []
player_group = []
enemy_group = []
timer_group = []
text_group = []
obstacle_group = []
button_group = []
list_group = []
conf_menu_group = []
extraction_group = []
drop_group = []
mission_group = []

#Helper Functions
def process_object_group(group, surface):
    for item in group:
        item.update()
        item.draw(surface)
        
def list_to_list(original_list, future_list):
    for item in original_list:
        future_list.append(item)
    return len(future_list)
    
def pack_menu(menu, asset_list):
    for item in asset_list:
        if isinstance(item, Button):
            menu.add_button(item)
        elif isinstance(item, Menu):
            menu.add_menu(item)
        elif isinstance(item, Text):
            menu.add_text(item)
        elif isinstance(item, Surface):
            menu.add_surface(item)
        elif isinstance(item, List_Block):
            menu.add_list(item)
        else:  
            menu.add_surface(item)
            
def number_to_text(number, dict):
    return dict[number]
    
def print_credits():
    pass

def remove_list_item(list_block, list_id): 
    for list_item in list_block.get_item_list():
        if list_item.get_id() == list_id:
            list_block.remove_item(list_item)
            
def create_confirmation_menu(text, pos, size, color, alpha, functions):
    conf_menu = Confirmation_Menu(text, pos, size, color, alpha, functions)
    conf_menu_group.append(conf_menu)    
    
def update_list_block(list_block, list, func):
    temp_list = []
    for item in list:
        list_item = List_Item(item.get_name(), list_block, item.get_color(), item.get_color(), 200, func, item)
        list_item.add_text(item.get_name(), [list_item.get_size()[0] * 0.3, list_item.get_size()[1] / 2], white, 20, "impact")
        list_item.add_text("Lvl " + str(item.get_level()), [list_item.get_size()[0] * 0.8, list_item.get_size()[1] / 2], white, 20, "impact")
        if isinstance(item, Weapon):
            list_item.add_mod_slots()    
        temp_list.append(list_item)
    list_block.set_list(temp_list)
        
def test_collisions(object, collision_list):
    for obstacle in collision_list:
        if object.collision([obstacle.get_pos()[0] + 5, obstacle.get_pos()[1], obstacle.get_size()[0] - 10, 10]):
            object.set_pos([object.get_pos()[0], obstacle.get_pos()[1] - object.get_size()[1]])
            object.set_vel([object.get_vel()[0], 0])
            object.set_jumpstacks(1)
        elif object.collision([obstacle.get_pos()[0], obstacle.get_pos()[1], 10, obstacle.get_size()[1]]):
            object.set_pos([obstacle.get_pos()[0] - object.get_size()[0], object.get_pos()[1]])
        elif object.collision([obstacle.get_pos()[0] + obstacle.get_size()[0] - 10, obstacle.get_pos()[1], 10, obstacle.get_size()[1]]):
            object.set_pos([obstacle.get_pos()[0] + obstacle.get_size()[0], object.get_pos()[1]])
            
def bullet_collisions(player, enemy, obstacle_list):
    for bullet in player.get_equipped_primary_weapon().get_bullet_list():
        for obstacle in obstacle_list:
            if bullet.collision([obstacle.get_pos()[0], obstacle.get_pos()[1], obstacle.get_size()[0], obstacle.get_size()[1]]):
                player.get_equipped_primary_weapon().remove_bullet(bullet)
            if bullet.collision([enemy.get_pos()[0], enemy.get_pos()[1], enemy.get_size()[0], enemy.get_size()[1]]):
                damage = bullet.get_damage()
                text_color = black
                if player.get_equipped_primary_weapon().get_crit_chance() > random.randrange(0,100):
                    damage *= player.get_equipped_primary_weapon().get_crit_mult()
                    text_color = purple
                if bullet.collision([enemy.get_pos()[0], enemy.get_pos()[1], enemy.get_size()[0], 30]):
                    damage *= player.get_equipped_primary_weapon().get_headshot_mult()
                    text_color = orange
                enemy.remove_health(damage)
                player.get_equipped_primary_weapon().remove_bullet(bullet)
                damage_text = Text(str(int(damage)), [random.choice([enemy.get_pos()[0] - 50, enemy.get_pos()[0] + enemy.get_size()[0] + 50]), enemy.get_pos()[1] + 10], text_color, 30, "impact", True, 20)
                text_group.append(damage_text)
                if enemy.get_current_health() <= 0:
                    return True
                else:
                    return False
                    
def set_selected_mission(mission):
    global selected_mission
    selected_mission = mission
    
def activate_selected_mission():
    global active_mission, selected_mission
    active_mission = [selected_mission]
    for mission in active_mission:
        mission.activate_mission()
    
type_dict = {0: "Assault Rifle", 1: "SMG", 2: "LMG", 3: "Shotgun", 4: "Sniper Rifle", 5: "Pistol"}      
      
#MAINLOOP
def main_loop(surface):
    global selected_mission, active_mission
    playing = True
    loop_count = 0
    
    player_image_list = [player_standing_img, player_standing_img_reverse, player_crouching_img, player_crouching_img_reverse]
    enemy_image_list = [rioter_standing_img, rioter_standing_img_reverse, rioter_crouching_img, rioter_crouching_img_reverse]
    
    #Create Objects
    weapon = Weapon("AK47", "better than arun", 0, 4, AK47_image, [30,10], 30, 900, 900, 900, 1, 10, 0, 2)
    weapon2 = Weapon("P90", "memes", 3, 3, P90_image, [30,10], 50, 1080, 450, 1080, 2, 20, 30, 2)    
    floor = gameObject([0, HEIGHT * 0.9], [WIDTH, HEIGHT * 0.1], (124,246,123))
    obstacle_group.append(floor)
    obs1 = gameObject([800,floor.get_pos()[1] - 100], [100,100], black)
    obs2 = gameObject([500,floor.get_pos()[1] - 100], [100,100], black)
    obs3 = gameObject([200,floor.get_pos()[1] - 100], [100,100], black)
    player = Player([50, HEIGHT * 0.9 - 150], [65, 150], 35, player_image_list, weapon, 90000, 0)
    player_group.append(player)
    
    #Create Missions
    mission1 = Mission("Madison Field Hospital", "Way too hard for Arun", 3, 1100, player)
    
    mission1.add_cover(obs1)
    mission1.add_cover(obs2)
    mission1.add_cover(obs3)
    
    enemy = Gunner([600,300], [65,150], 40, enemy_image_list, Weapon("AK47", "BLow STUFF UP", 0, 1, AK47_image, [30,10], 30, 800, 900, 900, 2, 10), 10000, 10, 20000, True, "Glass")
    enemy1 = Gunner([400,300], [65,150], 40, enemy_image_list, Weapon("AUG", "BLow STUFF UP", 0, 2, AK47_image, [30,10], 35, 900, 850, 950, 2, 10), 10000, 10)
    enemy2 = Gunner([800,300], [65,150], 40, enemy_image_list, Weapon("MP5", "BLow STUFF UP", 1, 3, P90_image, [30,10], 50, 2000, 700, 1300, 1, 10), 10000, 10)
    enemy3 = Rusher([400,300], [65,150], 40, enemy_image_list, Weapon("XM012", "BLow STUFF UP", 3, 4, XM_image, [30,10], 2, 200, 2000, 80, 3, 10), 10000, 10)
    enemy4 = Rusher([700,300], [65,150], 40, enemy_image_list, Weapon("Sawed Off", "BLow STUFF UP", 3, 1, XM_image, [30,10], 2, 100, 2000, 80, 2, 10), 10000, 10)
    enemy5 = Marksman([900,300], [65,150], 40, enemy_image_list, Weapon("Custom M44", "BLow STUFF UP", 4, 2, AWP_image, [30,10], 10, 200, 25000, 100, 3, 10), 10000, 10, 20000)
    enemy6 = Marksman([800,300], [65,150], 40, enemy_image_list, Weapon("Huntsman Rifle", "BLow STUFF UP", 4, 3, DEAGLE_image, [30,10], 14, 200, 18000, 300, 4, 10), 10000, 10, 20000)
    enemy7 = Marksman([600,300], [65,150], 40, enemy_image_list, Weapon("Custom M34", "BLow STUFF UP", 4, 4, AWP_image, [30,10], 7, 200, 50000, 20, 3, 10), 10000, 10, 20000, True, "Totomosic")
    
    mission1.add_enemy(enemy, 3)
    mission1.add_enemy(enemy1, 1)
    mission1.add_enemy(enemy2, 2)
    mission1.add_enemy(enemy3, 1)
    mission1.add_enemy(enemy4, 1)
    mission1.add_enemy(enemy5, 2)
    mission1.add_enemy(enemy6, 2)
    mission1.add_enemy(enemy7, 3)
    
    selected_mission = mission1
    active_mission = []
    
    #Extractable Items Menu
    extractable_items_menu = Menu([0,0], [WIDTH - 100, HEIGHT - 100], green, 128, False)
    
    title = Text("Extrable Items", [WIDTH * 0.45, HEIGHT * 0.1], white, 50, "impact")
    divider = gameObject([50, HEIGHT * 0.2], [extractable_items_menu.get_size()[0] - 100, 10], black)

    extract_group = List_Block([WIDTH * 0.07, HEIGHT * 0.27], [WIDTH * 0.4, HEIGHT * 0.5], red, 200, 5, 3)
    list_group.append(extract_group)
    
    pack_menu(extractable_items_menu, [title, divider, extract_group])
    
    #Primary Weapons Menu
    primary_weapons_menu = Menu([0,0], [WIDTH - 100, HEIGHT - 100], orange, 128, False)
    
    inventory_list = List_Block([WIDTH * 0.07, HEIGHT * 0.27], [WIDTH * 0.4, HEIGHT * 0.5], red, 200, 5, 3)
    list_group.append(inventory_list)
    player.add_inventory_item(weapon)
    player.add_inventory_item(weapon2)
    
    weapon_info = Button([WIDTH * 0.55, HEIGHT * 0.27], [WIDTH * 0.3, HEIGHT * 0.5], red, red, 128, [])
    weapon_info.add_text("Name: ", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.2], black, 30, "impact", True, False, [], lambda: player.get_selected_weapon().get_name())
    weapon_info.add_text("DPS: ", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.4], black, 30, "impact", True, False, [], lambda: player.get_selected_weapon().get_dps())
    weapon_info.add_text("Damage: ", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.6], black, 30, "impact", True, False, [], lambda: player.get_selected_weapon().get_damage())
    weapon_info.add_text("RPM: ", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.8], black, 30, "impact", True, False, [], lambda: player.get_selected_weapon().get_firerate())
    
    title = Text("Primary Weapons", [WIDTH * 0.45, HEIGHT * 0.1], white, 50, "impact")
    divider = gameObject([50, HEIGHT * 0.2], [primary_weapons_menu.get_size()[0] - 100, 10], black)
    
    equip_button = Button([WIDTH * 0.51, HEIGHT * 0.78], [WIDTH * 0.1, HEIGHT * 0.05], blue, (0,0,255), 128, [lambda: player.set_equipped_primary_weapon(player.get_selected_weapon())])
    equip_button.add_text("Equip", [equip_button.get_size()[0] / 2, equip_button.get_size()[1] / 2], white, 20, "impact")
    remove_button = Button([WIDTH * 0.62, HEIGHT * 0.78], [WIDTH * 0.16, HEIGHT * 0.05], red, (255,0,0), 128, [lambda: create_confirmation_menu("Are you sure you want to deconstruct the " + player.get_selected_weapon().get_name() + "?", [WIDTH * 0.2, HEIGHT * 0.1], [WIDTH * 0.6, HEIGHT * 0.1], purple, 200, [lambda: remove_list_item(inventory_list, player.get_selected_weapon().get_name()), lambda: player.remove_inventory_item(player.get_selected_weapon())])])
    remove_button.add_text("Deconstruct Item", [remove_button.get_size()[0] / 2, remove_button.get_size()[1] / 2], white, 20, "impact")
    mod_button = Button([WIDTH * 0.79, HEIGHT * 0.78], [WIDTH * 0.1, HEIGHT * 0.05], blue, (0,0,255), 128, [lambda: player.set_equipped_primary_weapon(player.get_selected_weapon())])
    mod_button.add_text("Mod", [mod_button.get_size()[0] / 2, mod_button.get_size()[1] / 2], white, 20, "impact")
    
    back_button = Button([WIDTH * 0.01, HEIGHT * 0.02], [50,20], green, (0,255,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    back_button.add_text("Back", [back_button.get_size()[0] / 2, back_button.get_size()[1] / 2], white, 15, "impact")
    
    pack_menu(primary_weapons_menu, [inventory_list, back_button, title, divider, weapon_info, equip_button, remove_button, mod_button])
    
    #Inventory menu
    inventory_menu = Menu([0,0], [WIDTH - 100, HEIGHT - 100], (255,200,200), 128, False)
    
    primary_weapons_button = Button([WIDTH * 0.04, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(primary_weapons_menu)])
    primary_weapons_button.add_text("Primary Weapons", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    extract_items_button = Button([WIDTH * 0.04, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(extractable_items_menu)])
    extract_items_button.add_text("Extractable Items", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    mask_armor_button = Button([WIDTH * 0.32, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    mask_armor_button.add_text("Masks", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    chest_armor_button = Button([WIDTH * 0.32, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    chest_armor_button.add_text("Chest Armor", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    backpack_armor_button = Button([WIDTH * 0.6, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    backpack_armor_button.add_text("Backpacks", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    gloves_armor_button = Button([WIDTH * 0.6, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    gloves_armor_button.add_text("Gloves", [primary_weapons_button.get_size()[0] / 2, primary_weapons_button.get_size()[1] / 2], white, 30, "impact")
    
    back_button = Button([WIDTH * 0.01, HEIGHT * 0.02], [50,20], green, (0,255,0), 200, [lambda: main_menu.set_selected_menu(main_menu)])
    back_button.add_text("Back", [back_button.get_size()[0] / 2, back_button.get_size()[1] / 2], white, 15, "impact")
    
    firearms_display = Button([WIDTH * 0.025, HEIGHT * 0.08], [WIDTH * 0.25, HEIGHT * 0.2], red, red, 150, [])
    firearms_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 1.2], white, 20, "impact", True, False, [], lambda: player.get_attributes()[0])
    firearms_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 2], white, 40, "impact", True, False, [], lambda: player.get_equipped_primary_weapon().get_dps())
    stamina_display = Button([WIDTH * 0.325, HEIGHT * 0.08], [WIDTH * 0.25, HEIGHT * 0.2], blue, blue, 150, [])
    stamina_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 1.2], white, 20, "impact", True, False, [], lambda: player.get_attributes()[1])
    stamina_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 2], white, 40, "impact", True, False, [], lambda: player.get_max_health())
    electronics_display = Button([WIDTH * 0.625, HEIGHT * 0.08], [WIDTH * 0.25, HEIGHT * 0.2], green, green, 150, [])
    electronics_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 2], white, 40, "impact", True, False, [], lambda: player.get_attributes()[2] * 10)
    electronics_display.add_text("", [firearms_display.get_size()[0] / 2, firearms_display.get_size()[1] / 1.2], white, 20, "impact", True, False, [], lambda: player.get_attributes()[2])
        
    divider = gameObject([50, HEIGHT * 0.33], [inventory_menu.get_size()[0] - 100, 10], black)
    
    pack_menu(inventory_menu, [back_button, extract_items_button, extractable_items_menu, primary_weapons_button, mask_armor_button, chest_armor_button, backpack_armor_button, gloves_armor_button, firearms_display, stamina_display, electronics_display, divider])
    
    #Mission Menu
    mission_menu = Menu([0,0], [WIDTH - 100, HEIGHT - 100], purple, 128, False)
    
    title = Text("Missions", [WIDTH * 0.45, HEIGHT * 0.1], white, 50, "impact")
    divider = gameObject([50, HEIGHT * 0.2], [primary_weapons_menu.get_size()[0] - 100, 10], black)
    back_button = Button([WIDTH * 0.01, HEIGHT * 0.02], [50,20], green, (0,255,0), 200, [lambda: main_menu.set_selected_menu(main_menu)])
    back_button.add_text("Back", [back_button.get_size()[0] / 2, back_button.get_size()[1] / 2], white, 15, "impact")
    
    play_button = Button([WIDTH * 0.63, HEIGHT * 0.78], [WIDTH * 0.14, HEIGHT * 0.05], red, (255,0,0), 128, [lambda: activate_selected_mission()])
    play_button.add_text("Play Mission", [play_button.get_size()[0] / 2, play_button.get_size()[1] / 2], white, 20, "impact")
    
    mission_info = Button([WIDTH * 0.55, HEIGHT * 0.27], [WIDTH * 0.3, HEIGHT * 0.5], red, red, 128, [])
    mission_info.add_text("", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.2], black, 30, "impact", True, False, [], lambda: selected_mission.get_name())
    mission_info.add_text("", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.4], black, 30, "impact", True, False, [], lambda: selected_mission.get_desc())
    mission_info.add_text("Rec level: ", [weapon_info.get_size()[0] / 2, weapon_info.get_size()[1] * 0.6], black, 30, "impact", True, False, [], lambda: selected_mission.get_level())    
    
    mission_list = List_Block([WIDTH * 0.07, HEIGHT * 0.27], [WIDTH * 0.4, HEIGHT * 0.5], blue, 200, 5, 3)
    list_group.append(mission_list)
    
    pack_menu(mission_menu, [mission_info, mission_list, title, divider, back_button, play_button])
    
    #MAIN Menu
    main_menu = Menu([50,50], [WIDTH - 100, HEIGHT - 100], blue, 128, False)
    
    author = Text("Jordan Morrison's", [WIDTH * 0.35, HEIGHT * 0.15], orange, 20, "impact")
    title = Text("The Multiplication", [WIDTH * 0.45, HEIGHT * 0.2], white, 50, "impact")
    divider = gameObject([50, HEIGHT * 0.3], [main_menu.get_size()[0] - 100, 10], black)
    
    close_button = Button([main_menu.get_size()[0] - 60, 10], [50,20], red, (255,0,0), 200, [lambda: main_menu.set_show(False), lambda: weapon_hud.set_show(True)])
    close_button.add_text("X", [25,10], white, 20, "tahoma")
    
    inventory_menu_button = Button([WIDTH * 0.32, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    inventory_menu_button.add_text("Inventory", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    inventory_menu_button.add_text("0/", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 1.2], white, 20, "impact", True, False, [], lambda: player.get_inventory_capacity())
    settings_menu_button = Button([WIDTH * 0.32, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    settings_menu_button.add_text("Settings", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    abilities_menu_button = Button([WIDTH * 0.04, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    abilities_menu_button.add_text("Abilities", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    missions_menu_button = Button([WIDTH * 0.6, HEIGHT * 0.6], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(mission_menu)])
    missions_menu_button.add_text("Missions", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    DZ_menu_button = Button([WIDTH * 0.04, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: main_menu.set_selected_menu(inventory_menu)])
    DZ_menu_button.add_text("Dark Zone", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    blank_menu_button = Button([WIDTH * 0.6, HEIGHT * 0.37], [WIDTH * 0.25, HEIGHT * 0.2], red, (255,0,0), 200, [lambda: print_credits()])
    blank_menu_button.add_text("Credits", [inventory_menu_button.get_size()[0] / 2, inventory_menu_button.get_size()[1] / 2], white, 30, "impact")
    
    pack_menu(main_menu, [inventory_menu, mission_menu, extractable_items_menu, primary_weapons_menu, author, title, divider, close_button, inventory_menu_button, settings_menu_button, abilities_menu_button, missions_menu_button, DZ_menu_button, blank_menu_button])
    menu_group.append(main_menu)
    
    #Weapon HUD Menu
    weapon_hud = Menu([WIDTH * 0.7, HEIGHT * 0.1], [WIDTH * 0.25, HEIGHT * 0.15], red, 200)
    weapon_hud.add_border()
    
    health_segment_1 = Loading_Bar([weapon_hud.get_size()[0] * 0.08, weapon_hud.get_size()[1] * 0.1], [75, 20], (0,255,0), black, 200, 255, 2, True, [], [lambda: player.get_current_health(), lambda: player.get_max_health() / 3.0])
    health_segment_2 = Loading_Bar([weapon_hud.get_size()[0] * 0.37, weapon_hud.get_size()[1] * 0.1], [76, 20], (0,255,0), black, 200, 255, 2, True, [], [lambda: player.get_current_health() - player.get_max_health() / 3.0, lambda: player.get_max_health() / 3.0])
    health_segment_3 = Loading_Bar([weapon_hud.get_size()[0] * 0.66, weapon_hud.get_size()[1] * 0.1], [75, 20], (0,255,0), black, 200, 255, 2, True, [], [lambda: player.get_current_health() - player.get_max_health() * 2 / 3.0, lambda: player.get_max_health() / 3.0])
    
    weapon_name_text = Text("", [weapon_hud.get_size()[0] * 0.3, weapon_hud.get_size()[1] * 0.55], white, 20, "impact", True, False, [], lambda: player.get_equipped_primary_weapon().get_name())
    weapon_type_text = Text("", [weapon_hud.get_size()[0] * 0.3, weapon_hud.get_size()[1] * 0.8], yellow, 20, "impact", True, False, [], lambda: number_to_text(player.get_equipped_primary_weapon().get_type(), type_dict))
    weapon_ammo_text = Text("", [weapon_hud.get_size()[0] * 0.7, weapon_hud.get_size()[1] * 0.55], white, 20, "impact", True, False, [], lambda: player.get_equipped_primary_weapon().get_current_ammo())
    weapon_max_ammo_text = Text("", [weapon_hud.get_size()[0] * 0.7, weapon_hud.get_size()[1] * 0.8], white, 20, "impact", True, False, [], lambda: player.get_equipped_primary_weapon().get_total_ammo())
    
    pack_menu(weapon_hud, [weapon_name_text, weapon_type_text, weapon_ammo_text, weapon_max_ammo_text, health_segment_1, health_segment_2, health_segment_3])
    menu_group.append(weapon_hud)
    
    #HUD Menu
    hud = Menu([0,0], [0,0], BG_COLOR, 0)
    
    xp_bar = Loading_Bar([WIDTH / 1.9, HEIGHT * 0.05], [WIDTH * 0.35, HEIGHT * 0.03], purple, black, 255, 255, 2, True, [], [lambda: player.get_xp(), lambda: player.get_xp_list()[player.get_level()]])
    level_text = Text("", [WIDTH * 0.935, HEIGHT * 0.065], black, 30, "impact", True, False, [], lambda: player.get_level())
    weapon_hud_close_button = Button([weapon_hud.get_pos()[0] + weapon_hud.get_size()[0], weapon_hud.get_pos()[1]], [WIDTH * 0.0252, WIDTH * 0.0252], blue, (0,0,255), 128, [lambda: weapon_hud.toggle_show()])
    toggle_text = Text("^", [weapon_hud.get_pos()[0] + weapon_hud.get_size()[0] * 0.65, weapon_hud.get_pos()[1]], black, 15, "tahoma")
    
    pack_menu(hud, [xp_bar, level_text, weapon_hud_close_button, toggle_text])
    menu_group.append(hud)
    
    update_list_block(inventory_list, player.get_inventory_list(), [player.set_selected_weapon])
    update_list_block(mission_list, [mission1], [set_selected_mission])
    
    while playing:
    
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        #Logic
        #Update Menus
        weapon_hud.set_pos([WIDTH * 0.6, xp_bar.get_pos()[1] + xp_bar.get_size()[1]])
        toggle_text.set_pos([weapon_hud.get_pos()[0] + weapon_hud.get_size()[0] + WIDTH * 0.01251, weapon_hud.get_pos()[1] + WIDTH * 0.01251])
        weapon_hud_close_button.set_pos([weapon_hud.get_pos()[0] + weapon_hud.get_size()[0], weapon_hud.get_pos()[1]])
        
        if main_menu.get_show():
            weapon_hud.set_show(False)
        
        if weapon_hud.get_show():
            toggle_text.set_text("v")
        else:
            toggle_text.set_text("^")
                
        for person in player_group:
            test_collisions(person, obstacle_group)
            if person.get_xp() >= person.get_xp_list()[person.get_level()]:
                player_level_up = pygame.USEREVENT + 1
                player_level_up_event = pygame.event.Event(player_level_up, person=person)
                pygame.event.post(player_level_up_event)
            
        for mission in active_mission:
            if mission.get_active():
                for enemy in mission.get_enemies():
                    test_collisions(enemy, obstacle_group)
                    test_collisions(enemy, mission.get_covers())
                test_collisions(player, mission.get_covers())
                
        for extraction in extraction_group:
            if player.collision([extraction.get_pos()[0] - 10, extraction.get_pos()[1] - 10, 20, 20]):
                for item in player.get_extracted_items():
                    player.add_inventory_item(item)   
                    player.remove_extracted_item(item)
                
        if player.get_update_inv():
            update_list_block(inventory_list, player.get_inventory_list(), [player.set_selected_weapon])    
            player.set_update_inv(False)  
            
        for drop in drop_group:
            if player.collision([drop.get_pos()[0], drop.get_pos()[1], drop.get_size()[0], drop.get_size()[1]]):
                for item in drop.get_items():
                    player.add_extracted_item(item)
                drop_group.remove(drop)
                update_list_block(extract_group, player.get_extracted_items(), [])
         
        #Bullet Detection     
        #Detection for enemies associated with a mission                  
        for mission in active_mission:
            if mission.get_active():
                for enemy in mission.get_enemies():
                    if bullet_collisions(player, enemy, mission.get_covers()):
                        if random.randrange(0,enemy.get_equipped_primary_weapon().get_rank() + 1) == 0:
                            drop = Drop([enemy.get_pos()[0] + 10, enemy.get_pos()[1] - 300], [enemy.get_size()[0] - 10, enemy.get_size()[1] + 300], enemy.get_equipped_primary_weapon().get_color(), 100, [enemy.get_equipped_primary_weapon()], 1800)
                            drop_group.append(drop)
                        mission.remove_enemy(enemy)
                        player.add_xp((enemy.get_level() + 1) * 10)
                    bullet_collisions(enemy, player, mission.get_covers())
                    
        #Detection for enemies with no association to missions
        for enemy in enemy_group:
            if bullet_collisions(player, enemy, obstacle_group):
                if random.randrange(0,enemy.get_equipped_primary_weapon().get_rank() + 1) == 0:
                    drop = Drop([enemy.get_pos()[0] + 10, enemy.get_pos()[1] - 300], [enemy.get_size()[0] - 10, enemy.get_size()[1] + 300], enemy.get_equipped_primary_weapon().get_color(), 100, [enemy.get_equipped_primary_weapon()], 1800)
                    drop_group.append(drop)
                enemy_group.remove(enemy)
            bullet_collisions(enemy, player, obstacle_group)
                                                   
        #Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == player_level_up:
                event.person.set_level(event.person.get_level() + 1)
                event.person.set_xp(event.person.get_xp() - event.person.get_xp_list()[event.person.get_level() - 1])
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.set_vel([-2, player.get_vel()[1]])
                if event.key == pygame.K_d:
                    player.set_vel([2, player.get_vel()[1]])
                if event.key == pygame.K_w:
                    player.jump(12)
                if event.key == pygame.K_LCTRL:
                    player.set_crouching(True)
                if event.key == pygame.K_SPACE:
                    player.set_shooting(True)
                if event.key == pygame.K_r:
                    player.force_reload()
                if event.key == pygame.K_e:
                    test_extraction = Extraction(player, [player.get_pos()[0],300], [WIDTH,HEIGHT], 90, 25)
                    extraction_group.append(test_extraction)
                
                if event.key == pygame.K_p:
                    main_menu.toggle_show()
                if event.key == pygame.K_ESCAPE:
                    main_menu.set_selected_menu(main_menu)
                    main_menu.set_show(False)
                    weapon_hud.set_show(True)
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.set_vel([0, player.get_vel()[1]])
                if event.key == pygame.K_d:
                    player.set_vel([0, player.get_vel()[1]])
                if event.key == pygame.K_LCTRL:
                    player.set_crouching(False)
                if event.key == pygame.K_SPACE:
                    player.set_shooting(False)
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                for list_block in list_group:
                    if mouse_pos[0] > list_block.get_pos()[0] and mouse_pos[0] < list_block.get_pos()[0] + list_block.get_size()[0]:
                        if mouse_pos[1] > list_block.get_pos()[1] and mouse_pos[1] < list_block.get_pos()[1] + list_block.get_size()[1]:
                            if event.button == 4:
                                list_block.scroll_list(-1)
                            if event.button == 5:
                                list_block.scroll_list(1)
                                     
        #Update Display
        surface.fill(BG_COLOR)
        
        pygame.draw.circle(surface, (0,0,0), [int(WIDTH * 0.935), int(HEIGHT * 0.065)], int(WIDTH * 0.03 + 5))
        pygame.draw.circle(surface, (255,153,153), [int(WIDTH * 0.935), int(HEIGHT * 0.065)], int(WIDTH * 0.03))
        
        floor.update()
        floor.draw(surface)
        
        if len(conf_menu_group) > 1:
            conf_menu_group.pop()
        for menu in conf_menu_group:
            if menu.get_response():
                conf_menu_group.remove(menu)
                
        if len(extraction_group) > 1:
            extraction_group.pop()
        for extraction in extraction_group:
            if extraction.update():
                extraction_group.remove(extraction)
            extraction.draw(surface)
            
        for drop in drop_group:
            if drop.update():
                drop_group.remove(drop)
            drop.draw(surface)
        
        process_object_group(active_mission, surface)
        process_object_group(player_group, surface)
        process_object_group(enemy_group, surface)
        cover_group = []
        for obstacle in obstacle_group:
            if obstacle != floor:
                cover_group.append(obstacle)
        for enemy in enemy_group:
            enemy.AI(cover_group, player)
        process_object_group(timer_group, surface)
        process_object_group(text_group, surface)
        process_object_group(obstacle_group, surface)
        process_object_group(button_group, surface)
        process_object_group(menu_group, surface)
        process_object_group(conf_menu_group, surface)
                
        pygame.display.update()
        clock.tick(Updates_per_second)
        
        loop_count += 1
        
main_loop(gameDisplay)
pygame.quit()
quit()
