import pygame
from random import randrange, randint, choice, choices
from sys import exit
from pygame.math import Vector2


vec = Vector2
# ========================================================================== initialize
pygame.init()
# pygame.mixer.init()

# hide mouse from game window
pygame.mouse.set_visible(False)
# ========================================================================== display size

S_W = 800
S_H = 600
SCREEN = pygame.display.set_mode((S_W, S_H))
TABLE_SIZE = 100

# ========================================================================== add icon
#programIcon = pygame.image.load('./src/assets/images/title_icon/baby_hat.png')
#pygame.display.set_icon(programIcon)

# ========================================================================== add caption
pygame.display.set_caption('*** The Shooter ***', 'default_icon')

# ========================================================================== global const
# clock frames
CLOCK = pygame.time.Clock()
FPS = 60
# ------------------------------

# draw background
def background_image(image, x=0, y=0, is_image_scaled=False):
    if not is_image_scaled:
        bg_image = pygame.image.load(image).convert() # convert make image fast
    else:
        bg_image = image.convert()  # convert make image fast
    # draw bg screen
    SCREEN.blit(bg_image, (x, y))


# create text
def text_creator(text='No Text', rgb_color=(255, 255, 255), x_pos=S_W // 2,
                 y_pos=S_H // 2, font_size=25, background=None, font_type=None, under_line=False):
    font = pygame.font.Font(font_type, font_size)
    if under_line:
        pygame.font.Font.set_underline(font, True)
    input_text = font.render(text, True, rgb_color, background)
    text_position = input_text.get_rect(midleft=(x_pos, y_pos))
    SCREEN.blit(input_text, text_position)
    return input_text.get_size()


# resize image
def scale_image(image, x_size, y_size):
    scaled_image = pygame.transform.scale(pygame.image.load(image), (x_size, y_size))
    return scaled_image.convert()


#  file read and write
def file_operation(file_path, option="['r' or 'w' or 'a']", row_number_to_read=0, text_to_write='empty row'):
    with open(file_path, option) as file:
        if option == 'r':
            return file.readlines()[row_number_to_read]
        if option == 'w':
            return file.write(text_to_write + '\n')


# check key pressed or released
def key_pressed(input_key=None):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[input_key]:  # pygame.K_SPACE
        return True
    return False


# check key pressed
def check_key_pressed(input_key):
    keysPressed = pygame.key.get_pressed()
    if keysPressed[input_key]:
        return True
    else:
        return False


# keyboard events for exit
def exit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

