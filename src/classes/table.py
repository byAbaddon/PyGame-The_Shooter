import pygame
from src.settings import text_creator, SCREEN,  S_W, S_H, TABLE_SIZE, CLOCK, scale_image


class Table:
    def __init__(self,all_spite_groups_dict, shooter):
        self.asg = all_spite_groups_dict
        self.shooter_data = shooter

    def draw_labels_and_table_data(self):
        font_size = 22
        font = './src/fonts/aAblasco.ttf'

        # label_score   'cornflowerblue'
        text_creator('Score:', 'goldenrod4', 20, S_H - 15, 20, None, font)
        text_creator(f' {self.shooter_data.points}', 'goldenrod4', 80, S_H - 15, font_size, None, font)


        # # label killed enemies
        text_creator('Targets:', 'crimson', 190, S_H - 15, 20, None, font)
        text_creator(f'{self.shooter_data.counter_targets}', 'crimson', 270, S_H - 15, font_size, None, font)


        # label bullets left
        text_creator('Bullets:', 'orange', 330, S_H - 15, font_size, None, font)
        for index in range(0, self.shooter_data.bullets_collection):
            fruit = './src/assets/images/bullets/bullet.png'
            SCREEN.blit(scale_image(fruit, 15, 15),(410 + index * 18, S_H - 22))

        # label level
        text_creator('Level:', 'deepskyblue4', 590, S_H - 15, font_size, None, font)
        text_creator(f'{self.shooter_data.level}', 'deepskyblue4', 655, S_H - 15, font_size - 2, None, font)

        # label FPS
        text_creator('FPS:', 'lightskyblue4', 720, S_H - 15, font_size - 4, None, font)
        text_creator(f'{int(CLOCK.get_fps())}', 'lightskyblue4', 765, S_H - 15, font_size - 4, None, font)


    @staticmethod
    def draw_frame():
        frame = pygame.Rect( 0, S_H - 30, S_W, 30)
        pygame.draw.rect(SCREEN, 'black', frame, )

    def update(self):
        self.draw_frame()
        self.draw_labels_and_table_data()




