import pygame

from src.settings import *
from src.classes.background import Background
from src.classes.sound import Sound
from src.classes.table import Table
from src.classes.enemy import Enemy, global_enemy_pos
from src.classes.shooter import Shooter



# ======================================================================== create Sprite groups

shooter_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.Group()


# # add to all_sprite_groups
all_spite_groups_dict = {'shooter': shooter_group, 'enemy': enemy_group,  }

# # ======================================================================= initialize  Classes
#

shooter = Shooter(all_spite_groups_dict)
enemy = Enemy(f'./src/assets/images/enemies/empty.png', 0, 0, shooter, False)

# # add to group
shooter_group.add(shooter)


# ==================================================================
table = Table(all_spite_groups_dict, shooter)

# Game State
class GameState(Sound):
    COOLDOWN = 1000  # milliseconds
    start_timer = pygame.time.get_ticks()
    picture_enemy_type = ''
    enemy_number = 1
    x_cor = y_cor = 0
    enemy = None
    enemy_index_pos = 0

    def __init__(self,):
        self.state = 'intro'
        self.background_picture = None
        self.start_game_counter = 3
        self.is_music_play = False
        self.is_start_game = False
        self.is_created_enemy = False
        self.is_created_bonus = False
        self.is_game_over = False
        self.is_show_table = True
        self.reset_current_game_data = False
        self.reset_all_data_for_new_game = False

    def game(self):

        # ---------------------------- if level complete
        if shooter.is_level_complete:
            all_spite_groups_dict['enemy'].empty()
            pygame.time.delay(3000)
            self.reset_current_game_data = True
            if shooter.level == 5:
                shooter.reset_all_data()
                Sound.stop_all_sounds()
                self.state = 'final_game'
            else:
                self.state = 'get_ready'

        # -----------------------------  Reset current data
        if self.reset_current_game_data:
            global_enemy_pos.clear()
            self.COOLDOWN = 1000
            self.background_picture = None
            self.is_music_play = False
            self.is_start_game = False
            self.is_created_enemy = False
            self.is_created_bonus = False
            self.is_game_over = False
            self.start_game_counter = 3
            shooter.reset_current_data()
            enemy_group.empty()
            shooter_group.empty()
            shooter_group.add(shooter)
            enemy_group.empty()

        # ----------------------------- start game
        if not self.is_start_game:
            Sound.stop_all_sounds()
            self.reset_current_game_data = False
            if shooter.level < 5:
                self.background_picture = Background(f'./src/assets/images/game_backgrounds/{shooter.level}.png')
                if shooter.level == 1:
                        Sound.game_music_level_1(self)
                        self.enemy_number = 4
                elif shooter.level == 2:
                        Sound.game_music_level_2(self)
                        self.enemy_number = 1
                elif shooter.level == 3:
                        Sound.game_music_level_3(self)
                        self.enemy_number = 4
                elif shooter.level == 4:
                    Sound.game_music_level_4(self)
                    self.enemy_number = 4
            else:
                self.background_picture = Background(f'./src/assets/images/backgrounds/bg_final.png')
                Sound.game_final_music(self)
                self.state = 'final_game'
            self.is_start_game = True
            return

        # # ------------- generate enemies
        if not self.is_created_enemy : # not
            position = ()
            time_now = pygame.time.get_ticks()
            if shooter.level == 4 : self.COOLDOWN = 500
            if time_now - self.start_timer > self.COOLDOWN:
                self.start_timer = time_now
                if len(enemy_group) < self.enemy_number:
                    # ------------------------------------------------- setting for level 1
                    if shooter.level == 1:
                        self.picture_enemy_type = f'./src/assets/images/balloons/{randint(1, 6)}.png'
                        self.x_cor = randint(60, S_W - 100)
                        self.y_cor = S_H - 240
                    # ------------------------------------------------- setting for level 2
                    elif shooter.level == 2:
                        if shooter.counter_targets < 20:
                            choices_pic = choices([2,3],weights=[7,1])[0] #2
                        else:
                            if shooter.counter_targets & 1:
                                choices_pic = choices([4, 3], weights=[7,1])[0]
                            else:
                                choices_pic = choices([5, 3], weights=[7, 1])[0]
                        self.picture_enemy_type = f'./src/assets/images/body_targets/{choices_pic}.png'
                        self.x_cor = randint(240, 525)
                        self.y_cor = S_H - 288
                    # ------------------------------------------------- setting for level 3
                    elif shooter.level == 3:
                        choices_pic = choices(['sniper', 'rifle', 'pistol', 'scared'], weights=[6, 3, 3, 3])[0]
                        if len([x for x in enemy_group if x.image.get_width() == 100]) == 1: # rifle double
                            choices_pic =  'sniper'
                        if len([x for x in enemy_group if x.image.get_height() == 181]) == 1: # pistol double
                            choices_pic = 'sniper'
                        self.picture_enemy_type = f'./src/assets/images/enemies/{choices_pic}.png'
                        if choices_pic == 'rifle':
                            self.x_cor, self.y_cor = (400, 475)
                        elif choices_pic == 'pistol':
                            self.x_cor, self.y_cor = (400, 150)
                        else:
                            rand_pos = randint(0,3)
                            positions = [(155, 155), (S_W - 130, 155), (155, S_H - 160), (S_W - 130, S_H - 155)]
                            self.x_cor, self.y_cor = positions[rand_pos]
                            self.enemy_index_pos = positions.index((self.x_cor, self.y_cor))
                    # ---------------------------------------------- setting for level 4
                    elif shooter.level == 4:
                        choices_pic = choices(['sniper', 'rifle', 'pistol', 'gas_mask','scared'], weights=[6, 3, 3, 3, 4])[0]
                        if choices_pic == 'scared':
                            choices_pic = choice(['scared', 'scared_2'])

                        if len([x for x in enemy_group if x.image.get_height() == 190]) == 1:  # rifle double
                            choices_pic = 'sniper'
                        if len([x for x in enemy_group if x.image.get_height() == 181]) == 1:  # pistol double
                            choices_pic = 'sniper'
                        if len([x for x in enemy_group if x.image.get_width() == 131]) == 1:  # gas_mask double
                            choices_pic = 'sniper'

                        if choices_pic == 'rifle':
                            self.x_cor, self.y_cor = (266, 540)
                        elif choices_pic == 'pistol':
                            self.x_cor, self.y_cor = (choice([260, 550]), 150)
                        elif choices_pic == 'gas_mask':
                            self.x_cor, self.y_cor = (choice([170, 695]), 335)
                            if self.x_cor == 695:
                                choices_pic = 'gas_mask_2'
                        else:
                            rand_pos = randint(0, 3)
                            positions = [(155, 110), (700, 110),(320,300),(540,300),(155, 495), (690, 495) ]
                            self.x_cor, self.y_cor = positions[rand_pos]
                            self.enemy_index_pos = positions.index((self.x_cor, self.y_cor))

                        self.picture_enemy_type = f'./src/assets/images/enemies/{choices_pic}.png'

                    # ---------------------------------------------------------------add new enemy by above settings
                    flip_img  = False
                    if self.enemy_index_pos & 1:
                        flip_img = True

                    new_enemy = Enemy(self.picture_enemy_type,self.x_cor, self.y_cor, shooter, flip_img)

                    if shooter.level < 3:
                        enemy_group.add(new_enemy)
                    else:
                        if (self.x_cor, self.y_cor) not in global_enemy_pos:
                            global_enemy_pos.append((self.x_cor, self.y_cor))
                            enemy_group.add(new_enemy)

        if shooter.is_pause:
            shooter.is_pause = False
            self.state = 'pause'

        if shooter.is_game_over:
            self.reset_all_data_for_new_game = True
            if shooter.is_killed_victim:
                Sound.no_voice(self)
                pygame.time.delay(500)
            Sound.stop_all_sounds()
            Sound.enemy_pistol(self)
            pygame.time.delay(300)
            Sound.shooter_death_voice(self)
            pygame.time.delay(1000)
            Sound.game_over_voice(self)
            pygame.time.delay(1500)
            Sound.game_over_music(self)
            self.state = 'game_over'

        # ----------------------------- NEW GAME  reset all data
        if self.reset_all_data_for_new_game:
            global_enemy_pos.clear()
            self.COOLDOWN = 1000
            self.picture_enemy_type = ''
            self.enemy_number = 1
            self.x_cor = 0
            self.y_cor = 0
            self.background_picture = None
            self.start_game_counter = 3
            self.is_music_play = False
            self.is_start_game = False
            self.is_created_enemy = False
            self.is_created_bonus = False
            self.is_game_over = False
            self.is_show_table = True
            self.reset_current_game_data = False
            enemy.reset_current_data()
            [all_spite_groups_dict[group].empty() for group in all_spite_groups_dict]
            shooter_group.add(shooter)
            shooter.reset_all_data()
            self.reset_all_data_for_new_game = False

        # # =================================================== UPDATE
        # Grid.draw_grid(self)
        try:
            self.background_picture.update() # highlight is bg None
            self.enemy.update()
        except: pass

        # ----------------------------- update table data
        if self.is_show_table:
            table.update()
        # #  --------------------------- draw sprite group

        enemy_group.draw(SCREEN)
        shooter_group.draw(SCREEN)

        # # --------------------------- update sprite group
        enemy_group.update()
        shooter_group.update()

        # text_creator(f'{pygame.mouse.get_pos()}', 'red', S_W // 5 / 10)

    def intro(self):
        if not self.is_music_play:
            Sound.stop_all_sounds()
            Sound.intro_music(self)
            self.is_music_play = True
        font = './src/fonts/aAblasco.ttf'
        background_image('./src/assets/images/backgrounds/bg_intro.png')
        text_creator('The Shooter', 'brown', 70, 60, 80, None, './src/fonts/born.ttf')
        text_creator('Menu - M', 'red', S_W - 230, S_H - 160, 30, None, font)
        text_creator('Credits - C', 'fuchsia', S_W - 230, S_H - 110, 30, None, font)
        text_creator('Start - SPACE', 'deepskyblue', S_W - 230, S_H - 60, 32, None, font)
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, font)
        text_creator('Copyright 2023', 'white', S_W - 125, S_H - 10, 15, None, font)

        if check_key_pressed(pygame.K_SPACE):
            Sound.btn_click(self)
            self.start_game_counter = 3
            Sound.stop_all_sounds()
            self.state = 'get_ready'
        if check_key_pressed(pygame.K_c):
            Sound.btn_click(self)
            self.state = 'credits'
        if check_key_pressed(pygame.K_m):
            Sound.btn_click(self)
            self.state = 'menu'
        exit_game()

    def menu(self):
        background_image('./src/assets/images/backgrounds/bg_menu.png')
        text_creator('Press RETURN to back...', 'bisque', S_W - 230, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')
        if check_key_pressed(pygame.K_RETURN):
            self.state = 'intro'
        exit_game()

    def credits(self):
        font = None
        size = 16
        # background_image('./src/assets/images/backgrounds/bg_EMPTY.png')
        text_creator('CREDITS', 'slateblue3', S_W // 2 - 100, 40, 50, None, './src/fonts/aAblasco.ttf', True)
        text_creator('version: 1.0.0-beta', 'cornsilk', S_W - 160, 20, 16, None, './src/fonts/aAblasco.ttf')

        text_creator('Free images:', 'brown', 110, 100, 35, None, font)
        text_creator('https://www.pngwing.com', 'cadetblue4', 130, 125, 30, None, font)

        text_creator('Free sounds:', 'brown', 110, 200, 35, None, font)
        text_creator('https://freesound.org/', 'cadetblue4', 130, 225, 30, None, font)

        text_creator('Platform 2D game:', 'brown', 110, S_H // 2, 34, None, font)
        text_creator('https://www.pygame.org', 'cadetblue4', 130, S_H // 2 + 24, 30, None, font)

        SCREEN.blit(pygame.image.load('./src/assets/images/title/pygame_logo.png'), (S_W // 4 - 50, S_H - 266))

        text_creator('Developer:', 'brown', 30, S_H - 60, 30, None, font)
        text_creator('by Abaddon', 'cadetblue4', 50, S_H - 40, 30, None, font)

        text_creator('Bug rapports:', 'brown', S_W // 2 - 90, S_H - 60, 30, None, font)
        text_creator('subtotal@abv.bg', 'cadetblue4', S_W // 2 - 70, S_H - 40, 30, None, font)

        text_creator('Copyright:', 'brown', S_W - 140, S_H - 60, 30, None, font)
        text_creator('© 2023', 'cadetblue4', S_W - 120, S_H - 40, 30, None, font)

        text_creator('Press RETURN to back...', 'bisque', S_W - 230, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if check_key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'intro'
        exit_game()

    def get_ready(self):
        Sound.stop_all_sounds()
        time_now = pygame.time.get_ticks()
        if time_now - self.start_timer > self.COOLDOWN:
            self.start_game_counter -= 1
            self.start_timer = time_now
        font = './src/fonts/aAblasco.ttf'
        background_image('./src/assets/images/backgrounds/bg_poster.png')
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, font)
        text_creator('Copyright 2023', 'white', S_W - 125, S_H - 10, 15, None, font)
        text_creator(f'START AFTER: {int(self.start_game_counter)}', 'grey55', 200, S_H - 40, 40, None, './src/fonts/born.ttf')

        if self.start_game_counter <= 0:
            self.is_start_game = False
            # self.is_start = True
            self.state = 'game'

    def start_pause(self):
        background_image('./src/assets/images/backgrounds/bg_pause.png')
        text_creator('PAUSE', 'red3', S_W // 2 - 30, S_H  // 2 - 30, 80, None, './src/fonts/born.ttf')
        text_creator('Press RETURN to continue...', 'bisque', S_W - 255, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if key_pressed(pygame.K_RETURN):
            self.state = 'game'

    def final_game(self):
        background_image('./src/assets/images/backgrounds/bg_final.png')
        text_creator('Congratulations', 'white', 170, 60, 40, None, './src/fonts/born.ttf', True)
        text_creator('MISSION COMPLETE SUCCESSFULLY', 'orange', 80, S_H - 100, 30, None, './src/fonts/aAblasco.ttf')
        text_creator('- Hostages are released.', 'darkgreen', 80, S_H - 60, 26, None, './src/fonts/aAblasco.ttf')
        text_creator('- All terrorists are eliminated.', 'firebrick2', 80, S_H - 20, 26, None, './src/fonts/aAblasco.ttf')
        text_creator('Press RETURN to back...', 'bisque', S_W - 230, S_H - 12, 20, None, './src/fonts/aAblasco.ttf')
        if check_key_pressed(pygame.K_RETURN):
            Sound.stop_all_sounds()
            Sound.intro_music(self)
            self.state = 'intro'
        exit_game()

    def game_over(self):
        background_image('./src/assets/images/backgrounds/bg_game_over.png',0, 75)
        text_creator('GAME OVER', 'white', S_W // 4, S_H // 2, 54, None, './src/fonts/born.ttf')
        text_creator('Press RETURN to back...', 'bisque', S_W - 240, S_H - 12, 20, None,'./src/fonts/aAblasco.ttf')

        if key_pressed(pygame.K_RETURN):
            Sound.stop_all_sounds()
            Sound.intro_music(self)
            self.reset_all_data_for_new_game = True
            self.state = 'intro'
        exit_game()

    # ========================================= state manager ...
    def state_manager(self):
        # print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'game':
            self.game()
        if self.state == 'get_ready':
            self.get_ready()
        if self.state == 'menu':
            self.menu()
        if self.state == 'credits':
            self.credits()
        if self.state == 'pause':
            self.start_pause()
        if self.state == 'final_game':
            self.final_game()
        if self.state == 'game_over':
            self.game_over()



#  ================================ create new GameState
game_state = GameState()


# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
