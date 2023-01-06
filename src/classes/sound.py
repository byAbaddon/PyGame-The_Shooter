import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)


class Sound:
    @staticmethod
    def play_sound(sound_file, volume=0.5, loops=0):
        play = pygame.mixer.Sound(sound_file)
        play.set_volume(volume)
        play.play(loops)

    @staticmethod
    def stop_all_sounds():
        pygame.mixer.stop()

    def btn_click(self):
        self.play_sound('./src/assets/sounds/btn_one.wav')

    # Background
    def intro_music(self):
        self.play_sound('./src/assets/sounds/intro_music.mp3', 0.6, -1)

    def background_music(self):
        self.play_sound('./src/assets/sounds/background_one.mp3', 0.6, -1)

    def game_music_level_1(self):
        self.play_sound('./src/assets/sounds/game_music_level_1.mp3', 0.8, - 1)

    def game_music_level_2(self):
        self.play_sound('./src/assets/sounds/game_music_level_2.mp3', 0.8, - 1)

    def game_music_level_3(self):
        self.play_sound('./src/assets/sounds/game_music_level_3.mp3', 0.5, - 1)

    def game_music_level_4(self):
        self.play_sound('./src/assets/sounds/game_music_level_4.wav', 0.8, - 1)

    def game_final_music(self):
        self.play_sound('./src/assets/sounds/game_final_music.mp3', 0.7, -1)

    def game_over_music(self):
        self.play_sound('./src/assets/sounds/game_over_music.mp3', 0.5, -1)

    def game_over_voice(self):
        self.play_sound('./src/assets/sounds/game_over_voice.wav', 0.9)

    def get_ready_voice(self):
        self.play_sound('./src/assets/sounds/get_ready_voice.wav')

    def bonus_music(self):
        self.play_sound('./src/assets/sounds/bonus_label.wav')
    # ------------------------------------------------------

    # ----------------------------------- guns ------------------
    def shooter_death_voice(self):
            self.play_sound('./src/assets/sounds/shooter_death_voice.wav')

    def no_voice(self):
        self.play_sound('./src/assets/sounds/no_voice.wav')

    def help_voice(self):
        self.play_sound('./src/assets/sounds/help_voice.wav', 0.2)

    def shooter_reloading_voice(self):
        self.play_sound('./src/assets/sounds/guns/reloading_voice.wav')

    def yes_voice(self):
        self.play_sound('./src/assets/sounds/yes_voice.wav')
    def are_you_crazy_voice(self):
        self.play_sound('./src/assets/sounds/are_you_crazy_voice.wav', 0.9)

    def shooter_pistol(self):
        self.play_sound('./src/assets/sounds/guns/shooter_pistol.wav')

    def reload_pistol(self):
        self.play_sound('./src/assets/sounds/guns/reload_pistol.wav')

    def enemy_pistol(self):
        self.play_sound('./src/assets/sounds/guns/enemy_pistol.wav', 0.9)

    def machine_gun(self):
            self.play_sound('./src/assets/sounds/guns/machine_gun.wav')

    # -------------------------------------------
    def add_bonus_points(self):
        self.play_sound('./src/assets/sounds/bonus.wav')

    def add_bonus_fruit(self):
        self.play_sound('./src/assets/sounds/bonus_add.mp3')