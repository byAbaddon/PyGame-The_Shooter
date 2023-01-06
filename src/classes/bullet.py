import pygame
from src.settings import vec

class Bullet(pygame.sprite.Sprite):
    speed = 1
    is_reversed_pic = False

    def __init__(self, all_spite_groups_dict, pacman, img=''):
        pygame.sprite.Sprite.__init__(self)
        self.asg = all_spite_groups_dict
        self.pacman_data = pacman
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (30, 30)
        self.direction = vec(0, -1)
        self.pos = vec(self.rect.x, self.rect.y)

    def move(self):
        self.rect.y += self.speed * self.direction.y
        self.rect.x += self.speed * self.direction.x

    def sprite_frames(self):
       pass


    def update(self):
        self.move()


