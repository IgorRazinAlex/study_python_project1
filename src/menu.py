import pygame
from os import path
from src.agreements import *


# Class for main menu screen
class MainMenu:
    def __init__(self, window=None):
        self.window = window
        self._init_image()
        self._init_text()

    def start_music(self):
        self.window.music.stop()
        self.window.music.play(pygame.mixer.Sound(
            path.join(DATA_PATH, SOUND_PATH, 'start_screen.wav')), loops=-1)
        self.window.music.set_volume(SOUND_LEVEL)

    def _init_image(self):
        self.background_image = pygame.image.load(
            path.join(DATA_PATH, IMAGE_PATH, BACKGROUND_PATH, 'cybercity.jpg'))
        self.background_image = pygame.transform.scale(self.background_image,
                                                       WINDOW_SIZE)
        self.fading_image = pygame.image.load(
            path.join(DATA_PATH, IMAGE_PATH, BACKGROUND_PATH, 'fading.png'))
        self.fading_image = pygame.transform.scale(self.fading_image,
                                                   WINDOW_SIZE)

    def _init_text(self):
        self.intro_text = ['Through the Time and Space',
                           'Press any key to continue']
        self.title_font = pygame.font.Font(
            pygame.font.match_font('lucidasans'), 72)
        self.title_y = 30
        self.title_speed = 0.01
        self.subtitle_font = pygame.font.Font(
            pygame.font.match_font('lucidaconsole'), 24)

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.running = False
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
                self.window.cur_screen = 'rules_screen'

    # Draws screen
    def _draw_screen(self):
        self._draw_image()
        self._draw_text()
        self.draw_fading()
        self._move_title()

    # Draws background
    def _draw_image(self):
        self.window.screen.blit(self.background_image, (0, 0))

    # Draws text and moves title
    def _draw_text(self):
        string_title = self.title_font.render(
            self.intro_text[0], True, pygame.Color('white'))
        string_subtitle = self.subtitle_font.render(
            self.intro_text[1], True, pygame.Color('white'))
        rect_title = string_title.get_rect()
        rect_subtitle = string_subtitle.get_rect()
        rect_title = rect_title.move(40, self.title_y)
        rect_subtitle = rect_subtitle.move(360, 500)
        self.window.screen.blit(string_title, rect_title)
        self.window.screen.blit(string_subtitle, rect_subtitle)

    # Moves title
    def _move_title(self):
        if 30 <= self.title_y <= 50:
            self.title_speed *= 1.01
            self.title_y += self.title_speed
        elif self.title_y < 30:
            self.title_speed = 0.01
            self.title_y = 30
        else:
            self.title_speed = -0.01
            self.title_y = 50

    # Draws fading
    def draw_fading(self):
        if self.fading_image.get_alpha() != 0:
            self.window.screen.blit(self.fading_image, (0, 0))
            self.fading_image.set_alpha(self.fading_image.get_alpha() - 0.125)
