import pygame
from src.settings import S_W , S_H, vec, text_creator, choice
from src.classes.sound import Sound

global_enemy_pos = []

class Enemy(pygame.sprite.Sprite, Sound):
    COOLDOWN = 1000
    start_time = pygame.time.get_ticks()
    time_counter = 0
    speed = 2
    is_change_direction = False
    is_help = False

    def __init__(self, img, x_pos, y_pos, shooter, flip_img=False):
        pygame.sprite.Sprite.__init__(self)
        self.shooter_data = shooter
        self.image = pygame.image.load(img)\
            if flip_img else pygame.transform.flip(pygame.image.load(img), True, False).convert_alpha()
        self.item_name = img.split('/')[5][:-4]
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x_pos, y_pos)
        self.direction = vec(0, 0)
        self.index_pos = 1

    def move(self):
        self.rect.y += self.speed * self.direction.y
        self.rect.x += self.speed * self.direction.x

    def set_position_enemy(self):
        # ---------------------------------------------------------- Level 1
        if self.shooter_data.level == 1:
            self.speed = 3
            self.rect.y -= self.speed  # move balloon to top with speed
            if self.rect.y < -self.image.get_height(): # prevent overflow
                self.kill()
        # ---------------------------------------------------------- Level 2
        if self.shooter_data.level == 2:
            self.speed = 2  # restore speed to default
            if self.shooter_data.counter_targets < 20:
                if self.time_counter > 1:
                    self.kill()
            else:
                if self.time_counter > 4:
                    self.kill()
                if self.shooter_data.counter_targets > 30:
                    self.speed = 5
                if self.shooter_data.counter_targets > 30:
                    self.speed = 7
                if 220 < self.rect.x and not self.is_change_direction:
                    self.direction.x = -1
                else:
                    self.is_change_direction = True

                if self.is_change_direction and self.rect.x < 480:
                    self.direction.x = 1
                else:
                    self.is_change_direction = False
        # ---------------------------------------------------------- Level 3
        if self.shooter_data.level == 3:
            self.speed = 2  # restore speed to default
        # ---------------------------------------------------------- Level 4
        if self.shooter_data.level == 4:
            self.speed = 2  # restore speed to default
            if self.item_name in  ['pistol', 'rifle','gas_mask', 'gas_mask_2']:
                if self.item_name == 'gas_mask' or self.item_name == 'gas_mask_2':
                    self.image = pygame.transform.scale(self.image, (80, 120))
                else:
                    self.image = pygame.transform.scale(self.image,(58,110))
            else:
                if self.item_name in ['scared', 'scared_2']:
                    self.image = pygame.transform.scale(self.image, (55, 55))
                else:
                    self.image = pygame.transform.scale(self.image,(75,43))

    def timer_to_kill(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_time > 1000:
            self.start_time = time_now
            self.time_counter += 1
        color = 'darkgreen'
        if self.time_counter > 2:
            color = 'brown'
        if  self.item_name in ['scared', 'scared_2']:
            if not self.is_help:
                Sound.help_voice(self)
                self.is_help = True
            text_creator(f'HELP', 'red', self.rect.midtop[0] - 20,self.rect.midtop[1] - 20, 20, None, './src/fonts/aAblasco.ttf')
        else:
            text_creator(f'{self.time_counter} : {str(time_now)[-3:]}', color, self.rect.midtop[0] -20, self.rect.midtop[1] - 20, 18, None,'./src/fonts/aAblasco.ttf' )
        # -------------------------  YOU ARE KILLED ---------------
        if self.time_counter > 2.5 and self.item_name in ['scared', 'scared_2']:
            try: global_enemy_pos.remove(self.rect.center)
            except: pass
            self.kill()
        elif self.time_counter > 3 and self.shooter_data.level > 2:
            self.shooter_data.is_dead = True

    def reset_current_data(self):
        self.COOLDOWN = 1000
        self.start_time = pygame.time.get_ticks()
        self.time_counter = 0
        self.speed = 2
        self.is_change_direction = False
        self.is_help = False

    def update(self):
        self.move()
        self.set_position_enemy()
        if self.shooter_data.level > 1:
            self.timer_to_kill()

        if self.shooter_data.is_counter_target_done:
            self.kill()
            self.shooter_data.asg['enemy'].empty()
            self.reset_current_data()




