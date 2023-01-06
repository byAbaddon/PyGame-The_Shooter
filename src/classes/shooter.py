import pygame

from src.settings import *
from src.classes.sound import Sound
from src.classes.enemy import Enemy, global_enemy_pos

class Shooter(pygame.sprite.Sprite, Sound):
    COOLDOWN = 1000
    start_timer = pygame.time.get_ticks()
    level = 1

    # reset current data
    bullets_collection = 8
    counter_targets = 0
    points = 0
    is_level_complete = False
    is_game_over = False
    is_pause = False
    is_dead = False
    is_killed_victim = False
    is_shooting_allowed = False
    is_counter_target_done = False

    def __init__(self, all_spite_groups_dict):
        pygame.sprite.Sprite.__init__(self)
        self.asg = all_spite_groups_dict
        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (S_W // 2, S_H // 2)
        self.direction = vec(0, 0)

    def move(self):
       # ---------------------------------------------- PAUSE
        if key_pressed(pygame.K_p):
            self.is_pause = True
        # ------------------------------------------ move mouse target
        self.rect.center = (pygame.mouse.get_pos())

        # ------------------------------------------ clicked left  btn mouse is allowed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.is_shooting_allowed = True
            else:
                self.is_shooting_allowed = False

        # ---------------------------click right btn mouse
        if self.bullets_collection == 0:
            text_creator('RELOAD !!!', 'red', S_W // 3, S_H // 2, 44, None, './src/fonts/born.ttf', True)
        if pygame.mouse.get_pressed()[2] and  self.bullets_collection == 0:
            self.bullets_collection = 8
            Sound.reload_pistol(self)

    def check_enemy_collide(self):
        for sprite in pygame.sprite.spritecollide(self, self.asg['enemy'], False, pygame.sprite.collide_mask):
            if sprite:
                if self.counter_targets < 0:
                    self.counter_targets = 0
                # ----------------------------------- LEVEL 1
                if self.level == 1:
                    if sprite.rect.bottom - 40 > self.rect.y > sprite.rect.top and \
                            sprite.rect.right > self.rect.x > sprite.rect.left:
                        self.image = pygame.image.load('./src/assets/images/target/red.png').convert_alpha()
                        if pygame.mouse.get_pressed()[0] and self.bullets_collection > 0 and self.is_shooting_allowed:  # shooting
                            sprite.kill()
                            Sound.shooter_pistol(self)
                            self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
                            self.counter_targets += 1
                            self.points += 100
                            self.bullets_collection -= 1
                            if self.bullets_collection == 0:  # finished bullets
                                Sound.shooter_reloading_voice(self)
                            if sprite.item_name == '6':  # wrong balloon shooting
                                Sound.are_you_crazy_voice(self)
                                self.counter_targets -= 3
                                self.points -= 1000
                                if self.points < 0:
                                    self.points = 0
                    else:
                        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()

                # ----------------------------------- LEVEL 2
                if self.level == 2:
                    is_shooting_allowed = False

                    if sprite.item_name == '3': # target police man
                        # and sprite.rect.bottom > self.rect.y > sprite.rect.top  and \
                        # sprite.rect.right > self.rect.x > sprite.rect.left:
                        is_shooting_allowed = True
                    if self.counter_targets <= 20: # first target #20
                        if sprite.rect.bottom - 60 > self.rect.y > sprite.rect.top + 60 and \
                                sprite.rect.right - 30 > self.rect.x > sprite.rect.left + 20:
                            is_shooting_allowed = True
                    else:
                        if sprite.item_name == '4': # target headshot
                            if sprite.rect.bottom - 150 > self.rect.y > sprite.rect.top - 15  and \
                                    sprite.rect.topright[0] > self.rect.x > sprite.rect.left + 20:
                                is_shooting_allowed = True
                        if sprite.item_name == '5': # target body
                            if sprite.rect.bottom - 70 > self.rect.y > sprite.rect.top + 60 and \
                                    sprite.rect.right - 60 > self.rect.x > sprite.rect.left + 20:
                                is_shooting_allowed = True

                    if is_shooting_allowed:
                        self.image = pygame.image.load('./src/assets/images/target/red.png').convert_alpha()
                        if pygame.mouse.get_pressed()[0] and self.bullets_collection > 0 and self.is_shooting_allowed:  # shooting
                            sprite.kill()
                            Sound.shooter_pistol(self)
                            self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
                            self.counter_targets += 1
                            self.points += 200
                            self.bullets_collection -= 1
                            if self.bullets_collection == 0:  # finished bullets
                                Sound.shooter_reloading_voice(self)
                            if sprite.item_name == '3':  # wrong target shooting
                                self.counter_targets -= 3
                                self.points -= 1000
                                if self.points < 0:
                                    self.points = 0
                                Sound.are_you_crazy_voice(self)
                    else:
                        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()

                # ----------------------------------- LEVEL 3
                if self.level == 3:
                    is_shooting_allowed = False
                    if sprite.item_name == 'scared':  # target police man
                        is_shooting_allowed = True
                    if sprite.item_name == 'sniper' and sprite.rect.left + 10 < self.rect.left\
                            and self.rect.right < sprite.rect.right - 10 \
                            and sprite.rect.top - 10 < self.rect.top and self.rect.bottom < sprite.rect.bottom:
                        is_shooting_allowed = True
                    if sprite.item_name == 'pistol' and\
                            sprite.rect.left + 10 < self.rect.left and self.rect.right < sprite.rect.right - 10 \
                            and sprite.rect.top - 10 < self.rect.top and self.rect.bottom < sprite.rect.bottom - 80:
                        is_shooting_allowed = True
                    if sprite.item_name == 'rifle' and \
                            sprite.rect.left + 10 < self.rect.left and self.rect.right < sprite.rect.right - 10 \
                            and sprite.rect.top - 10 < self.rect.top and self.rect.bottom < sprite.rect.bottom - 80:
                        is_shooting_allowed = True

                    if is_shooting_allowed:
                        self.image = pygame.image.load('./src/assets/images/target/red.png').convert_alpha()
                        #  -------------------  click left btn mouse
                        if pygame.mouse.get_pressed()[0] and self.bullets_collection > 0 and self.is_shooting_allowed:  # shooting
                            try:
                                global_enemy_pos.remove(sprite.rect.center)
                            except:
                                pass
                            sprite.kill()
                            self.counter_targets += 1
                            Sound.shooter_pistol(self)
                            self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
                            self.points += 500
                            self.bullets_collection -= 1
                            if self.bullets_collection == 0: # finished bullets
                                Sound.shooter_reloading_voice(self)
                            if sprite.item_name == 'scared':
                                self.is_killed_victim = True
                                self.is_dead = True
                    else:
                        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()

                # ----------------------------------- LEVEL 4
                if self.level == 4:
                    self.image = pygame.image.load('./src/assets/images/target/red.png').convert_alpha()
                    #  -------------------  click left btn mouse
                    if pygame.mouse.get_pressed()[0] and self.bullets_collection > 0 and self.is_shooting_allowed:  # shooting
                        try:
                            global_enemy_pos.remove(sprite.rect.center)
                        except:
                            pass
                        sprite.kill()
                        self.counter_targets += 1
                        Sound.shooter_pistol(self)
                        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
                        self.points += 500
                        self.bullets_collection -= 1
                        if self.bullets_collection == 0:  # finished bullets
                            Sound.shooter_reloading_voice(self)
                        if sprite.item_name in ['scared', 'scared_2']:
                            self.is_killed_victim = True
                            self.is_dead = True
                    else:
                        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()

    def check_is_level_complete(self):
        rank = ''
        x_pos = S_W // 2

        if self.counter_targets >= 51 and self.level < 3: # 50
            self.asg['enemy'].empty()
            self.is_counter_target_done = True
        elif self.counter_targets > 60 and self.level == 3: # 60
            self.asg['enemy'].empty()
            self.is_counter_target_done = True
        elif self.counter_targets >= 80:  # 80
            self.asg['enemy'].empty()
            self.is_counter_target_done = True
        if self.is_counter_target_done:
            Sound.yes_voice(self)
            if self.level == 1:
                rank = 'Amateur'
                x_pos = S_W // 4 - 20
            if self.level == 2:
                rank = 'PRO'
                x_pos = S_W // 4 + 15
            if self.level == 3 or self.level == 4:
                text_creator('MISSION COMPLETE SUCCESSFULLY', 'darkgreen', 80, S_H // 2, 30, None, './src/fonts/born.ttf', True)
            else:
                text_creator('LEVEL COMPLETE', 'orange', S_W // 4, S_H // 3, 40, None, './src/fonts/born.ttf', True)
                text_creator(f'RANK {rank} - DONE!', 'crimson', x_pos, S_H // 3 + 50, 30, None, './src/fonts/born.ttf', True)
            self.level += 1
            self.is_level_complete = True
        if self.level == 4:
            if self.counter_targets % 10 == 0 and self.counter_targets > 0:
                img = pygame.image.load('./src/assets/images/enemies/naked_lady.png')
                SCREEN.blit(img, (510, 430))
        if self.level >= 5:
            self.is_level_complete = True

    def check_is_death(self):
        if self.is_dead: # --------------- game over
            SCREEN.fill('black')
            background_image('src/assets/images/backgrounds/bg_dead.png')
            if self.is_killed_victim:
                text_creator('Mission Failed', 'yellow',S_W // 4, S_H // 2, 40, None, './src/fonts/born.ttf')
            else:
                text_creator('You was killed', 'yellow',S_W // 4 , S_H // 2, 40, None, './src/fonts/born.ttf')
            self.is_game_over = True

    def reset_current_data(self):
        self.bullets_collection = 8
        self.counter_targets = 0
        self.is_level_complete = False
        self.is_game_over = False
        self.is_pause = False
        self.is_dead = False
        self.is_killed_victim = False
        self.is_shooting_allowed = False
        self.is_counter_target_done = False
        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (S_W // 2, S_H // 2)
        self.direction = vec(0, 0)

    def reset_all_data(self):
        self.COOLDOWN = 1000
        self.level = 1
        self.bullets_collection = 8
        self.counter_targets = 0
        self.points = 0
        self.is_level_complete = False
        self.is_game_over = False
        self.is_pause = False
        self.is_dead = False
        self.is_killed_victim = False
        self.is_shooting_allowed = False
        self.is_counter_target_done = False
        self.image = pygame.image.load('./src/assets/images/target/blue.png').convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (S_W // 2, S_H // 2)
        self.direction = vec(0, 0)

    def update(self):
        self.move()
        self.check_enemy_collide()
        self.check_is_level_complete()
        self.check_is_death()



